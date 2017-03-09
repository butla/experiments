from collections import namedtuple
from functools import partial

import scrapy

APEX_META = 'apex_request_data'

ApexRequestData = namedtuple('ApexRequestData',
                             'cookie, p_instance, p_flow_id, p_flow_step_id, x01, x02')


class ApexDataMissingError(Exception):
    """Raised when a response doesn't have all the data required to create subsequent
    requests to Apex."""


class ForeignPrincipalsSpider(scrapy.Spider):
    name = 'foreign_principals'

    def start_requests(self):
        url = 'https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'
        yield scrapy.Request(url=url, callback=self.add_country_to_table)

    def add_country_to_table(self, response):
        """The display of the application we're scraping is stateful and based on Apache Apex.
        Here, we'll issue a call to add the country to entries in the list.

        The initial request will get the default number of entries (principals)
        with default formatting. The entries themselves won't be used, but we'll use the received
        cookies and IDs to create further requests.
        """
        apex_data = self._get_apex_data(response)
        partial_form_data = {
            'p_request': 'APXWGT',
            'p_widget_name': 'worksheet',
            'p_widget_mod': 'ACTION',
            'p_widget_action': 'BREAK',
            'x03': 'COUNTRY_NAME',
        }
        form_data = self._get_apex_manipulation_data(apex_data, partial_form_data)

        # simulating the call to Apex (JavaScript engine behind FARA's website) worksheet
        yield scrapy.FormRequest(url="https://efile.fara.gov/pls/apex/wwv_flow.show",
                                 formdata=form_data,
                                 headers={'Cookie': apex_data.cookie},
                                 meta={APEX_META: apex_data},
                                 callback=self.add_all_principals_to_list)

    def add_all_principals_to_list(self, response):
        """Another call to Apex - it will get the response with all the principals."""
        apex_data = response.meta[APEX_META]
        partial_form_data = {
            'p_request': 'APXWGT',
            'p_widget_num_return': '100000',
            'f01': 'apexir_CURRENT_SEARCH_COLUMN',
            'f01': 'apexir_SEARCH',
            'f01': 'apexir_NUM_ROWS',
            'f02': '',
            'f02': '',
            'f02': '15',
            'p_widget_name': 'worksheet',
            'p_widget_mod': 'PULL',
        }
        form_data = self._get_apex_manipulation_data(apex_data, partial_form_data)

        yield scrapy.FormRequest(url="https://efile.fara.gov/pls/apex/wwv_flow.show",
                                 formdata=form_data,
                                 headers={'Cookie': apex_data.cookie},
                                 callback=self.parse_principals)

    def parse_principals(self, response):
        """<tr class="even"><td headers="LINK"><a href="f&#x3F;p&#x3D;171&#x3A;200&#x3A;10568377462008&#x3A;&#x3A;NO&#x3A;RP,200&#x3A;P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY&#x3A;3690,Exhibit&#x25;20AB,TAIWAN" ><img src="/i/view.gif" alt="View Documents"></a></td><td  align="left" headers="FP_NAME">Taipei Economic & Cultural Representative Office in the U.S.</td><td  align="left" headers="FP_REG_DATE">08/28/1995</td><td  align="left" headers="ADDRESS_1">Washington&nbsp;&nbsp;</td><td  align="left" headers="STATE">DC</td><td  align="left" headers="COUNTRY_NAME">TAIWAN</td><td  align="left" headers="REGISTRANT_NAME">International Trade & Development Agency, Inc.</td><td  align="center" headers="REG_NUMBER">3690</td><td  align="left" headers="REG_DATE">06/13/1985</td></tr>"""
        even_rows = response.css('.even')
        odd_rows = response.css('.odd')

    def parse_principal_document_url(self, response):
        pass

    def _get_element_value(self, element_id, response):
        return response.xpath("//*[@id='{}']/@value".format(element_id)).extract_first()

    def _get_apex_data(self, response) -> ApexRequestData:
        """
        Args:
            response: An initial response from FARA.

        Returns:
           Data needed for subsequent requests scraped of the response
        """
        if 'cookie' in response.request.headers:
            cookie = response.request.headers['Cookie']
        else:
            raise ApexDataMissingError('No cookie in the request that originated'
                                       'the response given to parse.')
        get_value_for_id = partial(self._get_element_value, response=response)
        apex_data = ApexRequestData(cookie=cookie,
                                    p_instance=get_value_for_id('pInstance'),
                                    p_flow_id=get_value_for_id('pFlowId'),
                                    p_flow_step_id=get_value_for_id('pFlowStepId'),
                                    x01=get_value_for_id('apexir_WORKSHEET_ID'),
                                    x02=get_value_for_id('apexir_REPORT_ID'))

        for field, value in apex_data._asdict().items():
            if not value:
                raise ApexDataMissingError(f'{field} is missing from the response.')

        return apex_data

    def _get_apex_manipulation_data(self, apex_data, form_data) -> dict:
        """Prepares form data for a request that will manipulate the Apex worksheet."""
        form_data = {
            **form_data
            **apex_data._asdict()
        }
        del form_data['cookie']
        return form_data

    # pierwszy parse bierze ciastka i dane
    # drugi dodaje country
    # trzeci bierze pelna liste
    # czwarty poszczegolne elementy sklada do kupy

    # def parse_page1(self, response):
    #     item = MyItem()
    #     item['main_url'] = response.url
    #     request = scrapy.Request("http://www.example.com/some_page.html",
    #                              callback=self.parse_page2)
    #     request.meta['item'] = item
    #     yield request
    #
    # def parse_page2(self, response):
    #     item = response.meta['item']
    #     item['other_url'] = response.url
    #     yield item

    # TODO date ISODate
    # TODO scrapy remove tags (z adresu)