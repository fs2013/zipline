# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pandas import Timestamp

from zipline.assets import Equity, Future

from zipline.data.dispatch_bar_reader import (
    AssetDispatchMinuteBarReader,
    AssetDispatchSessionBarReader,
)
from zipline.data.resample import (
    MinuteResampleSessionBarReader,
    ReindexMinuteBarReader,
    ReindexSessionBarReader,
)
from zipline.testing.fixtures import (
    WithBcolzEquityMinuteBarReader,
    WithBcolzEquityDailyBarReader,
    WithBcolzFutureMinuteBarReader,
    ZiplineTestCase,
)


class AssetDispatchSessionBarTestCase(WithBcolzEquityDailyBarReader,
                                      WithBcolzFutureMinuteBarReader,
                                      ZiplineTestCase):

    TRADING_CALENDAR_STRS = ('CME', 'NYSE')
    TRADING_CALENDAR_PRIMARY_CAL = 'CME'

    START_DATE = Timestamp('2016-08-22', tz='UTC')
    END_DATE = Timestamp('2016-08-25', tz='UTC')

    @classmethod
    def init_class_fixtures(cls):
        super(AssetDispatchSessionBarTestCase, cls).init_class_fixtures()

        readers = {
            Equity: ReindexSessionBarReader(
                cls.trading_calendar,
                cls.bcolz_equity_daily_bar_reader,
                cls.START_DATE,
                cls.END_DATE),
            Future: MinuteResampleSessionBarReader(
                cls.trading_calendar,
                cls.bcolz_future_minute_bar_reader
            )
        }
        cls.dispatch_reader = AssetDispatchSessionBarReader(
            cls.trading_calendar,
            cls.asset_finder,
            readers
        )

    def test_foo(self):
        pass


class AssetDispatchMinuteBarTestCase(WithBcolzEquityMinuteBarReader,
                                     WithBcolzFutureMinuteBarReader,
                                     ZiplineTestCase):

    TRADING_CALENDAR_STRS = ('CME', 'NYSE')
    TRADING_CALENDAR_PRIMARY_CAL = 'CME'

    ASSET_FINDER_EQUITY_SIDS = 1, 2, 3

    START_DATE = Timestamp('2016-08-24', tz='UTC')
    END_DATE = Timestamp('2016-08-25', tz='UTC')

    @classmethod
    def init_class_fixtures(cls):
        super(AssetDispatchMinuteBarTestCase, cls).init_class_fixtures()

        readers = {
            Equity: ReindexMinuteBarReader(
                cls.trading_calendar,
                cls.bcolz_equity_minute_bar_reader,
                cls.START_DATE,
                cls.END_DATE),
            Future: cls.bcolz_future_minute_bar_reader
        }
        cls.dispatch_reader = AssetDispatchMinuteBarReader(
            cls.trading_calendar,
            cls.asset_finder,
            readers
        )

    def test_load_raw_arrays(self):
        m_open, m_close = self.trading_calendar.open_and_close_for_session(
            self.START_DATE)

        results = self.dispatch_reader.load_raw_arrays(
            ['open'], m_open, m_close, [1, 2, 3])

