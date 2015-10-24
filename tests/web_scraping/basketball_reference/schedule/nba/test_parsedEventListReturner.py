import lxml.html as html
from unittest import TestCase
from src.web_scraping.basketball_reference.schedule.nba.parsed_event_list_returner import ParsedEventListReturner
from src.persistence.model.event import Event
from src.web_scraping.basketball_reference.schedule.nba.raw_events_returner import RawEventsReturner


class TestRawEventsReturner(RawEventsReturner):

    @staticmethod
    def return_raw_events(raw_content):
        schedule_html = html.fromstring(raw_content)
        raw_html_events = schedule_html.xpath('//td')
        return raw_html_events

    def __init__(self):
        RawEventsReturner.__init__(self)


class TestParsedEventListReturner(TestCase):
    def test_expected(self):
        schedule_html = open("static/schedule.html").read()
        raw_events = TestRawEventsReturner.return_raw_events(schedule_html)
        parsed_event_list_result = ParsedEventListReturner.return_parsed_event_list(raw_events)

        assert parsed_event_list_result is not None
        assert 1230 == len(parsed_event_list_result)

        for event in parsed_event_list_result:
            assert isinstance(event, Event)
            assert event.home_team_name is not None
            assert event.visiting_team_name is not None
            assert event.start_time is not None