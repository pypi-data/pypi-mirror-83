#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A python wrapper for the UK Carbon Intensity API.

https://api.carbonintensity.org.uk/

MIT License

Copyright (c) 2020 Joshua Brooke

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EselfPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__ = 'Joshua Brooke'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'Joshua Brooke'
__email__ = 'joshua.brooke@nationalgrideso.com'
__status__ = 'Development'

import requests


class CarbonIntensityAPI:
    """
    Create an object containing carbon intensity API data.

    Constructors:
        date (str): - in the form YYYY-MM-DDTHH:mmZ (Default value = None)
        period (str): - containing an integer (Default value = None)
        start (str): - in the form YYYY-MM-DDTHH:mmZ (Default value = None)
        end (str): - in the form YYYY-MM-DDTHH:mmZ (Default value = None)
        block (str): - containing an integer (Default value = None)
        postcode (str): - containing Outward postcode (first part) only
                  (Default value = None)

    Returns:
        Returns an object contaning carbon intensity api data.

    Methods:
        intensity_now()
        window_now()
        intensity_today()
        window_today()
        intensity_date()
        window_date()
        intensity_fw24h()
        window_fw24h()
        intensity_fw48h()
        window_fw48h()
        intensity_pt24h()
        window_pt24h()
        intensity_period()
        window_period()
        stats()
        stats_block()
        generation()
        generation_pt24h()
        generation_from_to()
        regional_generation_from_to()
        postcode_generation_from_to()
        england()
        scotland()
        wales()
        region()
        region_fw24h()
        region_fw48h()
        region_pt24h()
        postcode_generation()
        postcode_intensity()
        postcode_fw24h()
        postcode_fw48h()
        postcode_pt24h()

    Attributes:
        date (str): Specified date for carbon intensity data.
        period (str): Specified period for carbon intensity data.
        start (str): Specified date and period for start of carbon intensity
                    data.
        end (str): Specified date and period for end of carbon intensity data.
        block (str): Block of time as number of hours to consoder.
        postcode (str): Outward postcode (first part) only for determining
                        regional carbon intensity data.
        regions (dict): Region codes and region dno shortnames.
        national_now (json): Current carbon intensity for GB this half hour.
        factors (json): List of carbon intensity factors.
        today (json): Current carbon Intensity for today.
        gen_now (json): Generation mix for current half hour.
        regional (json): Current carbon intensity for GB regions.
    """

    def __init__(self, date=None, period=None, start=None, end=None,
                 block=None, postcode=None):
        """
        Initialise the CarbonIntensityAPI object.

        Args:
            See Class CarbonIntensityAPI for constructors.

        Example:
            x = CarbonIntensityAPI(date='2020-08-25T15:30Z',
                                   period='5',
                                   start='2020-08-20T15:30Z',
                                   end='2020-08-22T15:30Z',
                                   block='2',
                                   postcode='CV5')
        """
        headers = {'Accept': 'application/json'}
        url = r'https://api.carbonintensity.org.uk/'
        intensity = r'intensity/'
        gen = r'generation/'
        regional = r'regional/'
        pcode = r'postcode/'
        regions = {'North Scotland': 0,
                   'South Scotland': 1,
                   'North West England': 2,
                   'North East England': 3,
                   'Yorkshire': 4,
                   'North Wales': 5,
                   'South Wales': 6,
                   'West Midlands': 7,
                   'East Midlands': 8,
                   'East England': 9,
                   'South West England': 10,
                   'South England': 11,
                   'London': 12,
                   'South East England': 13,
                   'England': 14,
                   'Scotland': 15,
                   'Wales': 16,
                   'GB': 17
                   }

        self.date = date
        self.period = period
        self.start = start
        self.end = end
        self.block = block
        self.postcode = postcode
        self.regions = regions
        self.national_now = requests.get(url + intensity,
                                         params={}, headers=headers).json()
        self.factors = requests.get(url + intensity + 'factors',
                                    params={}, headers=headers).json()
        self.today = requests.get(url + intensity + 'date',
                                  params={}, headers=headers).json()
        self.gen_now = requests.get(url + gen,
                                    params={}, headers=headers).json()
        self.regional = requests.get(url + regional,
                                     params={}, headers=headers).json()

        if date:
            self._date = requests.get(url + intensity + date,
                                      params={}, headers=headers).json()
            self._fw24h = requests.get(url + intensity + date + '/fw24h',
                                       params={}, headers=headers).json()
            self._fw48h = requests.get(url + intensity + date + '/fw48h',
                                       params={}, headers=headers).json()
            self._pt24h = requests.get(url + intensity + date + '/pt24h',
                                       params={}, headers=headers).json()
            self._gen_pt24h = requests.get(url + gen + date + '/pt24h',
                                           params={}, headers=headers).json()
            self._regional_fw24h = requests.get(url + regional + intensity +
                                                date + '/fw24h',
                                                params={},
                                                headers=headers).json()
            self._regional_fw48h = requests.get(url + regional + intensity +
                                                date + '/fw48h',
                                                params={},
                                                headers=headers).json()
            self._regional_pt24h = requests.get(url + regional + intensity +
                                                date + '/pt24h',
                                                params={},
                                                headers=headers).json()

            if postcode:
                self._regional_pcode_fw24h = requests.get(url + regional +
                                                          intensity +
                                                          date + '/fw24h/' +
                                                          pcode + postcode,
                                                          params={},
                                                          headers=headers
                                                          ).json()
                self._regional_pcode_fw48h = requests.get(url + regional +
                                                          intensity +
                                                          date + '/fw48h/' +
                                                          pcode + postcode,
                                                          params={},
                                                          headers=headers
                                                          ).json()
                self._regional_pcode_pt24h = requests.get(url + regional +
                                                          intensity +
                                                          date + '/pt24h/' +
                                                          pcode + postcode,
                                                          params={},
                                                          headers=headers
                                                          ).json()

        if period:
            self._period = requests.get(url + intensity + 'date/' +
                                        date + '/' + period,
                                        params={}, headers=headers).json()

        if start and end:
            #  Maybe redundant
            self._fromto = requests.get(url + intensity + start + '/' + end,
                                        params={}, headers=headers).json()
            self._gen_fromto = requests.get(url + gen + start + '/' + end,
                                            params={}, headers=headers).json()
            self._regional_fromto = requests.get(url + regional + intensity +
                                                 start + '/' + end,
                                                 params={},
                                                 headers=headers).json()
            if postcode:
                self._pcode_fromto = requests.get(url + regional + intensity +
                                                  start + '/' + end + '/' +
                                                  pcode + postcode,
                                                  params={},
                                                  headers=headers).json()
            if block:
                self._statistics_block = requests.get(url + intensity +
                                                      'stats/' + start + '/' +
                                                      end + '/' + block,
                                                      params={},
                                                      headers=headers).json()
            else:
                self._statistics = requests.get(url + intensity + 'stats/' +
                                                start + '/' + end, params={},
                                                headers=headers).json()
        if postcode:
            self._postcode = requests.get(url + regional + pcode + postcode,
                                          params={}, headers=headers).json()

    def intensity_now(self):
        """Return a dict of forecasted/actual carbon intensity right now."""
        return self.national_now['data'][0]['intensity']

    def window_now(self):
        """Return a tuple containing the current carbon intensity window."""
        return (self.national_now['data'][0]['from'],
                self.national_now['data'][0]['to'])

    def intensity_today(self):
        """Return a dict of forecasted/actual carbon intensity for today."""
        return self.today['data'][0]['intensity']

    def window_today(self):
        """Return a tuple containing the today's carbon intensity window."""
        return (self.today['data'][0]['from'],
                self.today['data'][len(self.today['data'])-1]['to'])

    def intensity_date(self):
        """
        Return a dict of carbon intensity for the specified date.

        Requirements:
            date != None
        """
        return self._date['data'][0]['intensity']

    def window_date(self):
        """
        Return a tuple containing the date's carbon intensity window.

        Requirements:
            date != None
        """
        return self._date['data'][0]['from'], self._date['data'][0]['to']

    def intensity_fw24h(self):
        """Return a dict of carbon intensity for 24h after specific date.

        Requirements:
            date != None
        """
        return self._fw24h['data'][0]['intensity']

    def window_fw24h(self):
        """Return a tuple containing the forward carbon intensity window.

        Requirements:
            date != None
        """
        return (self._fw24h['data'][0]['from'],
                self._fw24h['data'][len(self._fw24h['data'])-1]['to'])

    def intensity_fw48h(self):
        """Return a dict of carbon intensity for 48h after specific date.

        Requirements:
            date != None
        """
        return self._fw48h['data'][0]['intensity']

    def window_fw48h(self):
        """Return a tuple containing the forward carbon intensity window.

        Requirements:
            date != None
        """
        return (self._fw48h['data'][0]['from'],
                self._fw48h['data'][len(self._fw48h['data'])-1]['to'])

    def intensity_pt24h(self):
        """Return a dict of carbon intensity for 24h before specific date.

        Requirements:
            date != None
        """
        return self._pt24h['data'][0]['intensity']

    def window_pt24h(self):
        """Return a tuple containing the past carbon intensity window.

        Requirements:
            date != None
        """
        return (self._pt24h['data'][0]['from'],
                self._pt24h['data'][len(self._pt24h['data'])-1]['to'])

    def intensity_period(self):
        """Return a dict of forecasted/actual carbon intensity for period.

        Requirements:
            date != None
            period != None
        """
        return self._period['data'][0]['intensity']

    def window_period(self):
        """Return a tuple containing the carbon intensity period.

        Requirements:
            date != None
            period != None
        """
        return self._period['data'][0]['from'], self._period['data'][0]['to']

    def stats(self):
        """Return statistics for the time specified in start-end.

        Requirements:
            start != None
            end != None
        """
        return self._statistics['data'][0]

    def stats_block(self):
        """Return statistics for the block given.

        Requirements:
            start != None
            end != None
            block != None
        """
        return self._statistics_block['data'][0]

    def generation(self):
        """Return current generation mix."""
        return self.gen_now['data']['generationmix']

    def generation_pt24h(self):
        """Return generation mix for the past 24h for specific date.

        Requirements:
            date != None
        """
        return self._gen_pt24h['data']

    def generation_from_to(self):
        """Return window and generation in that window.

        Requirements:
            start != None
            end != None
        """
        return (self._gen_fromto['data'],
                self._gen_fromto['data'][0]['from'],
                self._gen_fromto['data'][len(self._gen_fromto['data'])-1]['to'])

    def regional_generation_from_to(self, shortname):
        """Return window and generation in that window for a region.

        Args:
            shortname (str): - Name of one of the regions specified in the
                               .regions attribute

        Requirements:
            start != None
            end != None
        """
        return ((self._regional_fromto['data'][0]
                 ['regions'][self.regions[shortname]]['generationmix']),
                self._regional_fromto['data'][0]['from'],
                (self._regional_fromto['data']
                 [len(self._regional_fromto['data'])-1]['to']))

    def postcode_generation_from_to(self):
        """Return window and generation in that window for a postcode.

        Requirements:
            start != None
            end != None
            postcode != None
        """
        return (self._pcode_fromto['data']['data'],
                self._regional_fromto['data'][0]['from'],
                (self._regional_fromto['data']
                 [len(self._regional_fromto['data'])-1]['to']))

    def england(self):
        """Return regional data for England."""
        return self.regional['data'][0]['regions'][14]

    def scotland(self):
        """Return regional data for Scotland."""
        return self.regional['data'][0]['regions'][15]

    def wales(self):
        """Return regional data for Wales."""
        return self.regional['data'][0]['regions'][16]

    def region(self, shortname):
        """Return regional data for specified region."""
        return self.regional['data'][0]['regions'][self.regions[shortname]]

    def region_fw24h(self, shortname):
        """Return regional data for specified region for 24h after date.

        Args:
            shortname (str): - Name of one of the regions specified in the
                               .regions attribute
        Requirements:
            date != None
        """
        return (self._regional_fw24h['data'][0]['regions']
                [self.regions[shortname]])

    def region_fw48h(self, shortname):
        """Return regional data for specified region for 48h after date.

        Args:
            shortname (str): - Name of one of the regions specified in the
                               .regions attribute
        Requirements:
            date != None
        """
        return (self._regional_fw48h['data'][0]['regions']
                [self.regions[shortname]])

    def region_pt24h(self, shortname):
        """Return regional data for specified region for 24h before date.

        Args:
            shortname (str): - Name of one of the regions specified in the
                               .regions attribute
        Requirements:
            date != None
        """
        return (self._regional_pt24h['data'][0]['regions']
                [self.regions[shortname]])

    def postcode_generation(self):
        """Return regional generation for specific postcode.

        Requirements:
            postcode != None
        """
        return self._postcode['data'][0]['data'][0]['generationmix']

    def postcode_intensity(self):
        """Return regional carbon intensity for specific postcode.

        Requirements:
            postcode != None
        """
        return self._postcode['data'][0]['data'][0]['intensity']

    def postcode_fw24h(self):
        """Return regional data for specific postcode for 24h after date.

        Requirements:
            date != None
            postcode != None
        """
        return self._regional_pcode_fw24h['data']

    def postcode_fw48h(self):
        """Return regional data for specific postcode for 48h after date.

        Requirements:
            date != None
            postcode != None
        """
        return self._regional_pcode_fw48h['data']

    def postcode_pt24h(self):
        """Return regional data for specific postcode for 24h before date.

        Requirements:
            date != None
            postcode != None
        """
        return self._regional_pcode_pt24h['data']
