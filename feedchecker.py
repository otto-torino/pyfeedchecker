import json
import logging

import grequests

logging.basicConfig(filename='.pyfeedchecker.log', level=logging.INFO)
logger = logging.getLogger(__name__)


class Checker():
    def __init__(self, input, output):
        self.json_path = input
        self.output_path = output
        self.corrected_json = []

    def hook_factory(self, site):
        def response_hook(response, *request_args, **request_kwargs):
            logger.info('Checking %s' % response.url)
            logger.info(
                'Elapsed Time: %.2f' % response.elapsed.total_seconds())
            logger.info('Status Code: %d' % response.status_code)
            # keep only 200 <= codes < 300
            # redirects (3XX) causes this hook to be fired again, so are
            # not taken into account
            if (response.status_code < 300):
                self.corrected_json.append(site)

            return response

        return response_hook

    def run(self):

        total = 0
        totals = {}
        bad_results = 0

        with open(self.json_path) as f:
            sites = json.load(f)

        rs = (grequests.head(
            s.get('url'), hooks={'response': [self.hook_factory(s)]})
              for s in sites.get('base_urls'))
        for r in grequests.imap(rs, size=20):
            total += 1
            if totals.get(r.status_code):
                totals[r.status_code] += 1
            else:
                totals[r.status_code] = 1
            if r.status_code >= 400:
                bad_results += 1

        logger.info('Summary')
        logger.info('Total Requests: %d' % total)
        logger.info('Bad Responses: %d' % bad_results)
        for sc in totals:
            logger.info('Status Code %d: %d' % (sc, totals[sc]))

        self.write_corrected_json()

    def write_corrected_json(self):
        with open(self.output_path, 'w') as outfile:
            json.dump(
                self.corrected_json,
                outfile,
                sort_keys=True,
                indent=4,
                ensure_ascii=False)

    def get_corrected_json(self):
        return self.corrected_json
