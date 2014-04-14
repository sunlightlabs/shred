import time
import re

import requests
from shred import Command
import lxml, lxml.html

class NextbusPredictor(object):
    """Tracks Nextbus arrival times"""
    def __init__(self, routes):
        super(NextbusPredictor, self).__init__()
        self.routes = map(lambda x: str(x), routes.keys())
        self.route_urls = routes.copy()
        self.predictions = {}
        self.last_refresh = {}
        for r in self.routes:
            self.predictions[r] = None
            self.last_refresh[r] = None
            self.refresh(r)
    
    def _clean_prediction_html(self, html):
        return re.sub(r'&nbsp;','', re.sub(r'<[^>]*>','',(str(html)), flags=re.MULTILINE|re.DOTALL)).strip()

    def _extract_predictions(self, html):
        if '<p class="predictHead"><nobr><span id=\'i18n_en\'>No current prediction' in html:
            return None
        else:
            predictions = []
            nb_lxml = lxml.html.fromstring(html)

            # get the primary/imminent prediction          
            minutes = self._clean_prediction_html(nb_lxml.cssselect(".predictionNumberForFirstPred .right")[0].text.strip())    
            if ('departing' in minutes.lower()) or ('arriving' in minutes.lower()):
                predictions.append(0)
            else:
                predictions.append(int(minutes))

            # get the other predictions
            for m in nb_lxml.cssselect(".predictionNumberForOtherPreds .right"):
                m = self._clean_prediction_html(m.text.strip())
                try:
                    predictions.append(int(m))
                except:
                    pass

            return predictions

    def refresh(self, route):
        """Force a refresh of a specific route"""
        route = str(route)

        url = self.route_urls.get(str(route), False)
        if not url:
            return

        try:
            html = requests.get(url).content
        except:
            return # fail silently. bad, I know.

        self.predictions[route] = self._extract_predictions(html)
        self.last_refresh[route] = time.time()

    def _get_query_frequency(self, last_prediction_in_minutes):
        if last_prediction_in_minutes>20:
            return (last_prediction_in_minutes / 2) * 60
        elif last_prediction_in_minutes>10:
            return 3 * 60
        elif last_prediction_in_minutes>5:
            return 2 * 60
        else:
            return 60

    def refresh_if_necessary(self):
        """Only refresh prediction times intermittently -- don't hammer"""
        for r in self.routes:
            if self.predictions[r] is None:
                if (time.time() - self.last_refresh[r]) > TIMEOUT:
                    self.refresh(r)
            else:
                # if we have a prediction, refresh if we're halfway or more to
                # the expected arrival time
                if (time.time() - self.last_refresh[r]) > self._get_query_frequency(self.predictions[r][0]):
                    self.refresh(r)
    
    def _adjust_prediction_for_elapsed_time(self, prediction, r):
        return round(prediction - round((time.time() - self.last_refresh[r]) / 60.0))

    def get_closest_arrival(self):
        return self.get_nth_closest_arrival(0)

    def get_nth_closest_arrival(self, n=0, route=None):
        """Return the (route, arrival) pair that's happening soonest"""
        arrivals = []
        for r in self.routes:           
            if self.predictions.get(r) is not None:         
                for p in self.predictions.get(r, []):
                    valid_route = route is None
                    valid_route = valid_route or ((type(route) in (tuple, list)) and (r in route))
                    valid_route = valid_route or route==r
                    if valid_route:
                        arrivals.append( (p, r) )

        if n>=len(arrivals):
            return None

        matching_arrival = sorted(arrivals, key=lambda x: x[0])[n]
        return (matching_arrival[1], self._adjust_prediction_for_elapsed_time(matching_arrival[0], matching_arrival[1]))


class G2EastCommand(Command):

    COMMAND = 'g2east'

    def __call__(self, *args, **kwargs):

        nbp = NextbusPredictor({'G2': 'http://www.nextbus.com/predictor/fancyBookmarkablePredictionLayer.shtml?a=wmata&stopId=1001436&r=G2&d=G2_G2_0&s=6465'})
        nbp.refresh('G2')
        next_prediction = None
        i = 0
        while next_prediction is None and i<3:        
            next_prediction = nbp.get_nth_closest_arrival(i)
            i = i + 1

        if next_prediction is None:
            return "No prediction."
        else:
            return "Next bus in %s minutes." % int(next_prediction[1])


if __name__ == '__main__':
    g = G2EastCommand()
    print g()
