from pathlib import Path

import pytest
import scrapy.http

import fara.spiders.foreign_principals_spider as fp


@pytest.fixture
def cookie():
    return (b'ORA_WWV_APP_171=ORA_WWV-XqNjkEVwL8e59+x4oFH9Jq6A; '
            b'TS013766ce=016889935c959ab1dbcfa51d5613b357f43a3a5f'
            b'c0f8837be9c2e1c68a040be07ec939e88ba07bda52bfece55437b8000604c7d35e')


@pytest.fixture
def initial_response(cookie):
    body_file_path = (Path(__file__) / '../resources/first_response_body.html').resolve()
    with open(body_file_path, 'rb') as body_file:
        body = body_file.read()

    url = 'https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'
    request = scrapy.http.Request(url=url,
                                  headers={b'Cookie': cookie})
    response_headers = {
        b'Date': [b'Thu, 09 Mar 2017 01:17:32 GMT'],
        b'X-Db-Content-Length': [b'45331'],
        b'P3P': [b'policyref="/w3c/p3p.xml", CP="NOI DSP COR NID CUR ADM DEV OUR BUS"'],
        b'Content-Type': [b'text/html; charset=UTF-8'],
        b'Content-Language': [b'en']}

    return scrapy.http.HtmlResponse(
        url='https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N',
        headers=response_headers,
        request=request,
        body=body)


@pytest.fixture
def spider():
    return fp.ForeignPrincipalsSpider()


def test_add_country_to_table(cookie, initial_response, spider):
    outgoing_request = next(spider.add_country_to_table(initial_response))

    # I know we're not testing fully here, but we're still mostly testing the implementation.
    # Functional tests (with something like Betamax) would be needed.
    assert outgoing_request.url == 'https://efile.fara.gov/pls/apex/wwv_flow.show'
    assert outgoing_request.method == 'POST'
    assert b'p_instance=402061397258' in outgoing_request.body
    assert isinstance(outgoing_request.meta[fp.APEX_META], fp.ApexRequestData)
    assert outgoing_request.headers['cookie'] == cookie


def test_get_element_value(spider):
    response_body = b"""<tr>
    <td id="bla" value="nothing">something</td>
    <td id="ham" value="spam">blabla</td></tr>"""
    response = scrapy.http.HtmlResponse(url='https://bla', body=response_body)

    assert spider._get_element_value('ham', response) == 'spam'


def test_get_apex_data(cookie, spider):
    proper_apex_data = fp.ApexRequestData(cookie=cookie, p_flow_id='123', p_flow_step_id='234',
                                          p_instance='345', x01='456', x02='567')
    request = scrapy.http.Request(url='https://bla',
                                  headers={b'Cookie': cookie})
    response_body = f"""<tr>
        <td id="pFlowId" value="{proper_apex_data.p_flow_id}">x</td>
        <td id="pFlowStepId" value="{proper_apex_data.p_flow_step_id}">x</td>
        <td id="pInstance" value="{proper_apex_data.p_instance}">x</td>
        <td id="apexir_WORKSHEET_ID" value="{proper_apex_data.x01}">x</td>
        <td id="apexir_REPORT_ID" value="{proper_apex_data.x02}">x</td></tr>"""
    response = scrapy.http.HtmlResponse(url='https://bla', body=response_body.encode(),
                                        request=request)

    assert spider._get_apex_data(response) == proper_apex_data


def test_get_apex_data_with_missing_cookie(spider):
    response = scrapy.http.HtmlResponse(url='https://bla', body=b'<tr>bla</tr>',
                                        request=scrapy.http.Request(url='https://bla'))
    with pytest.raises(fp.ApexDataMissingError):
        spider._get_apex_data(response)


def test_get_apex_data_with_missing_ids(spider):
    request = scrapy.http.Request(url='https://bla', headers={'cookie': 'blabla'})
    response = scrapy.http.HtmlResponse(url='https://bla', body=b'<tr>bla</tr>',
                                        request=request)

    with pytest.raises(fp.ApexDataMissingError):
        spider._get_apex_data(response)
