"""Benchmark modules"""
import logging
import statistics
import random
from tempfile import SpooledTemporaryFile
from faker import Faker
from os_benchmark import utils, errors
from os_benchmark.drivers import errors as driver_errors


class BaseBenchmark:
    """Base Benchmark class"""
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('osb')
        self.params = {}

    def set_params(self, **kwargs):
        """Set test parameters"""
        self.params.update(kwargs)

    def setup(self):
        """Build benchmark environment"""

    def tear_down(self):
        """Destroy benchmark environment"""

    def run(self, **kwargs):
        """Run benchmark"""
        raise NotImplementedError()

    def make_stats(self):
        """Compute statistics as dict"""
        return {}


class UploadBenchmark(BaseBenchmark):
    """Time objects uploading"""
    def setup(self):
        self.timings = []
        self.objects = []
        self.errors = []
        self.driver.setup(**self.params)

        bucket_name = utils.get_random_name()
        self.storage_class = self.params.get('storage_class')
        self.logger.debug("Creating bucket '%s'", bucket_name)
        self.bucket = self.driver.create_bucket(
            name=bucket_name,
            storage_class=self.storage_class,
        )

    def run(self, **kwargs):
        def upload_files():
            for i in range(self.params['object_number']):
                name = utils.get_random_name()
                content = utils.get_random_content(self.params['object_size'])

                self.logger.debug("Uploading object '%s'", name)
                try:
                    elapsed, obj = utils.timeit(
                        self.driver.upload,
                        bucket_id=self.bucket['id'],
                        storage_class=self.storage_class,
                        name=name,
                        content=content,
                        multipart_threshold=self.params['multipart_threshold'],
                        multipart_chunksize=self.params['multipart_chunksize'],
                        max_concurrency=self.params['max_concurrency'],
                    )
                    self.timings.append(elapsed)
                    self.objects.append(obj)
                except driver_errors.DriverConnectionError as err:
                    self.logger.error(err)
                    self.errors.append(err)


        self.total_time = utils.timeit(upload_files)[0]

    def tear_down(self):
        self.driver.clean_bucket(bucket_id=self.bucket['id'])

    def make_stats(self):
        count = len(self.timings)
        error_count = len(self.errors)
        size = self.params['object_size']
        total_size = count * size
        test_time = sum(self.timings)
        rate = (count/test_time) if test_time else 0
        bw = (total_size/test_time/2**20) if test_time else 0
        stats = {
            'operation': 'upload',
            'ops': count,
            'time': self.total_time,
            'bw': bw,
            'rate': rate,
            'object_size': size,
            'object_number': self.params['object_number'],
            'multipart_threshold': self.params['multipart_threshold'],
            'multipart_chunksize': self.params['multipart_chunksize'],
            'max_concurrency': self.params['max_concurrency'],
            'total_size': total_size,
            'test_time': test_time,
            'errors': error_count,
            'driver': self.driver.id,
            'read_timeout': self.driver.read_timeout,
            'connect_timeout': self.driver.connect_timeout,
        }
        if count > 1:
            stats.update({
                'avg': statistics.mean(self.timings),
                'stddev': statistics.stdev(self.timings),
                'med': statistics.median(self.timings),
                'min': min(self.timings),
                'max': max(self.timings),
            })
        return stats


class DownloadBenchmark(BaseBenchmark):
    """Time objects downloading"""

    def setup(self):
        self.timings = []
        self.errors = []
        self.objects = []
        bucket_name = utils.get_random_name()
        self.logger.debug("Creating bucket '%s'", bucket_name)
        self.storage_class = self.params.get('storage_class')
        self.bucket = self.driver.create_bucket(
            name=bucket_name,
            storage_class=self.storage_class,
        )
        self.bucket_id = self.bucket['id']
        for i in range(self.params['object_number']):
            name = utils.get_random_name()
            content = utils.get_random_content(self.params['object_size'])

            self.logger.debug("Uploading object '%s'", name)
            try:
                obj = self.driver.upload(
                    bucket_id=self.bucket_id,
                    storage_class=self.storage_class,
                    name=name,
                    content=content,
                )
            except driver_errors.DriverError as err:
                self.logger.warning("Error during file uploading, tearing down the environment.")
                self.tear_down()
                raise
            self.objects.append(obj)
        self.urls = [
            self.driver.get_url(
                bucket_id=self.bucket_id,
                name=obj['name'],
                bucket_name=self.bucket.get('name', self.bucket_id),
            )
            for obj in self.objects
        ]
        self.logger.debug("URL(s): %s",  self.urls)

    def run(self, **kwargs):
        def download_objets(urls):
            for url in urls:
                try:
                    elapsed = utils.timeit(
                        self.driver.download,
                        url=url,
                    )[0]
                    self.timings.append(elapsed)
                except errors.InvalidHttpCode as err:
                    self.errors.append(err)

        self.total_time = utils.timeit(download_objets, urls=self.urls)[0]

    def tear_down(self):
        self.driver.clean_bucket(bucket_id=self.bucket['id'])

    def make_stats(self):
        count = len(self.timings)
        error_count = len(self.errors)
        size = self.params['object_size']
        total_size = count * size
        test_time = sum(self.timings)
        bw = (total_size/test_time/2**20) if test_time else 0
        rate = (count/test_time) if test_time else 0
        stats = {
            'operation': 'download',
            'ops': count,
            'time': self.total_time,
            'bw': bw,
            'rate': rate,
            'object_size': size,
            'object_number': self.params['object_number'],
            'max_concurrency': 1,
            'multipart_threshold': 0,
            'multipart_chunksize': 0,
            'total_size': total_size,
            'test_time': test_time,
            'errors': error_count,
            'driver': self.driver.id,
            'read_timeout': self.driver.read_timeout,
            'connect_timeout': self.driver.connect_timeout,
        }
        if count > 1:
            stats.update({
                'avg': statistics.mean(self.timings),
                'stddev': statistics.stdev(self.timings),
                'med': statistics.median(self.timings),
                'min': min(self.timings),
                'max': max(self.timings),
            })
        if error_count:
            error_codes = set([e for e in self.errors])
            stats.update({'error_count_%s' % e.args[1]: 0 for e in self.errors})
            for err in self.errors:
                key = 'error_count_%s' % err.args[1]
                stats[key] += 1
        return stats


class SqlBenchmark(BaseBenchmark):
    """Time objects uploading"""
    def  _generate_row(self, columns):
        row = []
        for col in columns:
            if col.startswith('str'):
                row.append(self.faker.user_name())
            elif col.startswith('int'):
                row.append(random.randint(0, 2**40))
            else:
                row.append(random.random())

        return row

    def _generate_rows(self, columns, rows):
        self.column_names = [
            ('%s_%s' % (c, self.faker.pystr()))
            for i, c in enumerate(columns)
        ]
        yield self.column_names
        for i in range(rows):
            yield self._generate_row(columns)

    def  _generate_object(self, format, columns, rows):
        obj = SpooledTemporaryFile(mode='rw')
        rows = self._generate_rows(columns, rows)
        for row in rows:
            line = ','.join([str(c) for c in row]) + '\n'
            obj.write(line)
        obj.seek(0)
        return obj

    def setup(self):
        self.timings = []
        self.objects = []
        self.errors = []

        random.seed(self.params.get('random-seed'))
        Faker.seed(self.params.get('random-seed'))
        self.faker = Faker()

        self.format = self.params.get('format', 'csv')
        self.expression = self.params['expression']

        self.driver.setup(**self.params)

        self.bucket_name = utils.get_random_name()
        self.object_name = '%s.%s' % (
            utils.get_random_name(),
            self.format,
        )
        self.storage_class = self.params.get('storage_class')
        self.rows = self.params.get('rows') or 5
        self.columns = self.params.get('columns', 'str').split(',')

        self.logger.debug("Creating bucket '%s'", self.bucket_name)
        self.bucket = self.driver.create_bucket(
            name=self.bucket_name,
            storage_class=self.storage_class,
        )

        self.logger.debug("Creating object '%s'", self.object_name)
        content = self._generate_object(
            format=self.format,
            columns=self.columns,
            rows=self.rows,
        )

        self.logger.debug("Uploading object '%s'", self.object_name)
        try:
            self.object = self.driver.upload(
                bucket_id=self.bucket['id'],
                storage_class=self.storage_class,
                name=self.object_name,
                content=content,
            )
        except driver_errors.DriverError as err:
            self.logger.warning("Error during file uploading, tearing down the environment.")
            self.tear_down()
            raise

    def run(self, **kwargs):
        def sql_select():
            self.logger.debug("Requesting '%s/%s'", self.bucket['id'], self.object)
            try:
                elapsed, _ = utils.timeit(
                    self.driver.sql_select,
                    bucket_id=self.bucket['id'],
                    name=self.object,
                    expression=self.expression,
                )
                self.timings.append(elapsed)
            except driver_errors.DriverConnectionError as err:
                self.logger.error(err)
                self.errors.append(err)

        self.total_time = utils.timeit(sql_select)[0]

    def tear_down(self):
        self.driver.clean_bucket(bucket_id=self.bucket['id'])

    def make_stats(self):
        count = len(self.timings)
        error_count = len(self.errors)
        stats = {
            'operation': 'sql',
            'expression': self.expression,
            'time': self.total_time,
            'test_time': self.timings[0],
            'rows': self.rows,
            'columns': ','.join(self.columns),
            'errors': error_count,
            'driver': self.driver.id,
            'read_timeout': self.driver.read_timeout,
            'connect_timeout': self.driver.connect_timeout,
        }
        if count > 1:
            stats.update({
                'avg': statistics.mean(self.timings),
                'stddev': statistics.stdev(self.timings),
                'med': statistics.median(self.timings),
                'min': min(self.timings),
                'max': max(self.timings),
            })
        return stats


class DownloadBenchmark(BaseBenchmark):
    """Time objects downloading"""

    def setup(self):
        self.timings = []
        self.errors = []
        self.objects = []
        bucket_name = utils.get_random_name()
        self.logger.debug("Creating bucket '%s'", bucket_name)
        self.storage_class = self.params.get('storage_class')
        self.bucket = self.driver.create_bucket(
            name=bucket_name,
            storage_class=self.storage_class,
        )
        self.bucket_id = self.bucket['id']
        for i in range(self.params['object_number']):
            name = utils.get_random_name()
            content = utils.get_random_content(self.params['object_size'])

            self.logger.debug("Uploading object '%s'", name)
            try:
                obj = self.driver.upload(
                    bucket_id=self.bucket_id,
                    storage_class=self.storage_class,
                    name=name,
                    content=content,
                )
            except driver_errors.DriverError as err:
                self.logger.warning("Error during file uploading, tearing down the environment.")
                self.tear_down()
                raise
            self.objects.append(obj)
        self.urls = [
            self.driver.get_url(
                bucket_id=self.bucket_id,
                name=obj['name'],
                bucket_name=self.bucket.get('name', self.bucket_id),
            )
            for obj in self.objects
        ]

    def run(self, **kwargs):
        def download_objets(urls):
            for url in urls:
                try:
                    elapsed = utils.timeit(
                        self.driver.download,
                        url=url,
                    )[0]
                    self.timings.append(elapsed)
                except errors.InvalidHttpCode as err:
                    self.errors.append(err)

        self.total_time = utils.timeit(download_objets, urls=self.urls)[0]

    def tear_down(self):
        self.driver.clean_bucket(bucket_id=self.bucket['id'])

    def make_stats(self):
        count = len(self.timings)
        error_count = len(self.errors)
        size = self.params['object_size']
        total_size = count * size
        test_time = sum(self.timings)
        bw = (total_size/test_time/2**20) if test_time else 0
        rate = (count/test_time) if test_time else 0
        stats = {
            'operation': 'download',
            'ops': count,
            'time': self.total_time,
            'bw': bw,
            'rate': rate,
            'object_size': size,
            'object_number': self.params['object_number'],
            'max_concurrency': 1,
            'multipart_threshold': 0,
            'multipart_chunksize': 0,
            'total_size': total_size,
            'test_time': test_time,
            'errors': error_count,
            'driver': self.driver.id,
            'read_timeout': self.driver.read_timeout,
            'connect_timeout': self.driver.connect_timeout,
        }
        if count > 1:
            stats.update({
                'avg': statistics.mean(self.timings),
                'stddev': statistics.stdev(self.timings),
                'med': statistics.median(self.timings),
                'min': min(self.timings),
                'max': max(self.timings),
            })
        if error_count:
            error_codes = set([e for e in self.errors])
            stats.update({'error_count_%s' % e.args[1]: 0 for e in self.errors})
            for err in self.errors:
                key = 'error_count_%s' % err.args[1]
                stats[key] += 1
        return stats
