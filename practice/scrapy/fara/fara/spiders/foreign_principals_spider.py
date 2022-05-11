from collections import namedtuple
from functools import partial
import itertools

import scrapy

from fara.items import ForeignPrincipalItem

APEX_META = 'apex_request_data'
ITEM_META = 'item'

ApexRequestData = namedtuple('ApexRequestData',
                             'cookie, p_instance, p_flow_id, p_flow_step_id, x01, x02')


class ApexDataMissingError(Exception):
    """Raised when a response doesn't have all the data required to create subsequent
    requests to Apex."""


class ForeignPrincipalsSpider(scrapy.Spider):
    name = 'foreign_principals'

    def start_requests(self):
        url = 'https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'
        yield scrapy.Request(url=url, callback=self.add_country_to_table, dont_filter=True)

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
            **form_data,
            **(apex_data._asdict()),
        }
        del form_data['cookie']
        return form_data


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
            'f01': ['apexir_CURRENT_SEARCH_COLUMN', 'apexir_SEARCH', 'apexir_NUM_ROWS'],
            'f02': ['', '', '15'],
            'p_widget_name': 'worksheet',
            'p_widget_mod': 'PULL',
        }
        form_data = self._get_apex_manipulation_data(apex_data, partial_form_data)

        yield scrapy.FormRequest(url="https://efile.fara.gov/pls/apex/wwv_flow.show",
                                 formdata=form_data,
                                 headers={'Cookie': apex_data.cookie},
                                 meta={APEX_META: apex_data},
                                 callback=self.parse_principals,
                                 dont_filter=True)

    def _get_item_from_row(self, row, response):
        relative_url = row.css('[headers="LINK"] > a::attr(href)').extract_first()
        url = response.urljoin(relative_url)
        return ForeignPrincipalItem(
            url=url,
            country = row.css('[headers="COUNTRY_NAME"]::text').extract_first(),
            state = row.css('[headers="STATE"]::text').extract_first(),
            reg_num = row.css('[headers="REG_NUMBER"]::text').extract_first(),
            address = row.css('[headers="ADDRESS_1"]::text').extract_first(),
            foreign_principal = row.css('[headers="FP_NAME"]::text').extract_first(),
            # TODO date as isodate
            date = row.css('[headers="FP_REG_DATE"]::text').extract_first(),
            registrant = row.css('[headers="REGISTRANT_NAME"]::text').extract_first())

    def parse_principals(self, response):
        apex_data = response.meta[APEX_META]
        even_rows = response.css('.even')
        odd_rows = response.css('.odd')

        for row in itertools.chain(even_rows, odd_rows):
            partial_foreign_principal = self._get_item_from_row(row, response)
            yield scrapy.Request(url=partial_foreign_principal['url'],
                                 callback=self.parse_principal_document_url,
                                 meta={APEX_META: apex_data, ITEM_META: partial_foreign_principal},
                                 headers={'Cookie': apex_data.cookie},
                                 dont_filter=True)

    def parse_principal_document_url(self, response):
        fp_item = response.meta[ITEM_META]
        even_rows = response.css('.even')
        odd_rows = response.css('.odd')
        exibit_urls = []

        for row in itertools.chain(even_rows, odd_rows):
            exibit_url = row.css('[headers="DOCLINK"] > a::attr(href)').extract_first()
            if exibit_url:
                exibit_urls.append(exibit_url)
        fp_item['exhibit_url'] = exibit_urls

        yield fp_item

    # TODO date ISODate