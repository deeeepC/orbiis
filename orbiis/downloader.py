import os
import urllib.request
from urllib.parse import urlparse
import gzip
from core.constants import SECS_IN_DAY, SECS_IN_WEEK
from orbiis.epoch import GPSTime 
from datetime import datetime
from unlzw import unlzw


def get_cache_path(url):
    if os.environ.get('CI', False):
        return url
    parsed_url = urlparse(url)
    return 'http://ftpcache.comma.life/' + parsed_url.netloc.replace(".", "-") + parsed_url.path


def fetch_file(url_base, folder, cache_dir, filename, compression='', overwrite=False):
    full_folder_path = os.path.join(cache_dir, folder)
    zipped_filename = filename + compression
    file_path = os.path.join(full_folder_path, filename)
    zipped_file_path = os.path.join(full_folder_path, zipped_filename)

    download_url = url_base + folder + zipped_filename
    download_url = get_cache_path(download_url)

    if not os.path.isfile(file_path) or overwrite:
        print(f"Downloading from {download_url} to {file_path}")
        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)
        try:
            response = urllib.request.urlopen(download_url)
            zipped_data = response.read()
            with open(zipped_file_path, 'wb') as zipped_file:
                zipped_file.write(zipped_data)

            if compression == '':
                return zipped_file_path
            elif compression == '.gz':
                with gzip.open(zipped_file_path, 'rb') as gz_file:
                    uncompressed_data = gz_file.read()
            elif compression == '.Z':
                with open(zipped_file_path, 'r') as z_file:
                    uncompressed_data = unlzw(z_file.read())
            else:
                raise NotImplementedError(f"Compression type {compression} not supported.")

            with open(file_path, 'w') as file:
                file.write(uncompressed_data)

        except IOError as e:
            print(f"Download failed: {e}")
            raise IOError(f"Failed to download file from: {download_url}")

    return file_path


def fetch_navigation_data(time, cache_dir, constellation='GPS'):
    timestamp = time.as_datetime()
    try:
        if GPSTime.from_datetime(datetime.utcnow()) - time > SECS_IN_DAY:
            base_url = 'ftp://cddis.gsfc.nasa.gov/gnss/data/daily/'
            cache_subdir = os.path.join(cache_dir, 'daily_nav/')
            if constellation == 'GPS':
                filename = timestamp.strftime("brdc%j0.%yn")
                folder = timestamp.strftime('%Y/%j/%yn/')
            elif constellation == 'GLONASS':
                filename = timestamp.strftime("brdc%j0.%yg")
                folder = timestamp.strftime('%Y/%j/%yg/')
            return fetch_file(base_url, folder, cache_subdir, filename, compression='.Z')
        else:
            base_url = 'ftp://cddis.gsfc.nasa.gov/gnss/data/hourly/'
            cache_subdir = os.path.join(cache_dir, 'hourly_nav/')
            if constellation == 'GPS':
                filename = timestamp.strftime("hour%j0.%yn")
                folder = timestamp.strftime('%Y/%j/')
                return fetch_file(base_url, folder, cache_subdir, filename, compression='.Z', overwrite=True)
    except IOError:
        pass


def fetch_orbit_data(time, cache_dir):
    cache_subdir = os.path.join(cache_dir, 'cddis_products/')
    base_url = 'ftp://cddis.gsfc.nasa.gov/gnss/products/'
    downloaded_files = []

    for t in [time - SECS_IN_DAY, time, time + SECS_IN_DAY]:
        folder = f"{t.week}/"
        if GPSTime.from_datetime(datetime.utcnow()) - t > 3 * SECS_IN_WEEK:
            try:
                filename = f"igs{t.week}{t.day}.sp3"
                downloaded_files.append(fetch_file(base_url, folder, cache_subdir, filename, compression='.Z'))
                continue
            except IOError:
                pass

        try:
            filename = f"igr{t.week}{t.day}.sp3"
            downloaded_files.append(fetch_file(base_url, folder, cache_subdir, filename, compression='.Z'))
        except IOError:
            pass
        for i in range(0, 19, 6):
            try:
                filename = f"igu{t.week}{t.day}_{i:02d}.sp3"
                downloaded_files.append(fetch_file(base_url, folder, cache_subdir, filename, compression='.Z'))
            except IOError:
                pass

    return downloaded_files


def fetch_russian_orbit_data(time, cache_dir):
    cache_subdir = os.path.join(cache_dir, 'russian_products/')
    base_url = 'ftp://ftp.glonass-iac.ru/MCC/PRODUCTS/'
    downloaded_files = []
    for t in [time - SECS_IN_DAY, time, time + SECS_IN_DAY]:
        dt = t.as_datetime()
        if GPSTime.from_datetime(datetime.utcnow()) - t > 2 * SECS_IN_WEEK:
            try:
                folder = dt.strftime('%y%j/final/')
                filename = f"Sta{t.week}{t.day}.sp3"
                downloaded_files.append(fetch_file(base_url, folder, cache_subdir, filename))
            except IOError:
                pass
        for interval in ['rapid', 'ultra']:
            try:
                folder = dt.strftime(f'%y%j/{interval}/')
                filename = f"Sta{t.week}{t.day}.sp3"
                downloaded_files.append(fetch_file(base_url, folder, cache_subdir, filename))
            except IOError:
                pass

    return downloaded_files


def fetch_ionex_data(time, cache_dir):
    cache_subdir = os.path.join(cache_dir, 'ionex/')
    dt = time.as_datetime()
    base_url = 'ftp://cddis.gsfc.nasa.gov/gnss/products/ionex/'
    folder = dt.strftime('%Y/%j/')
    filenames = [dt.strftime(f"codg%j0.%yi"), dt.strftime(f"c1pg%j0.%yi"), dt.strftime(f"c2pg%j0.%yi")]

    for filename in filenames:
        try:
            return fetch_file(base_url, folder, cache_subdir, filename, compression='.Z')
        except IOError as e:
            last_err = e

    raise last_err


def fetch_dcb_data(time, cache_dir):
    cache_subdir = os.path.join(cache_dir, 'dcb/')
    base_url = 'ftp://cddis.nasa.gov/gnss/products/bias/'
    last_err = None

    for t in [time - i * SECS_IN_DAY for i in range(14)]:
        try:
            dt = t.as_datetime()
            folder = dt.strftime('%Y/')
            filename = dt.strftime("CAS0MGXRAP_%Y%j0000_01D_01D_DCB.BSX")
            return fetch_file(base_url, folder, cache_subdir, filename, compression='.gz')
        except IOError as e:
            last_err = e

    raise last_err


def fetch_cors_coordinates(cache_dir):
    cache_subdir = os.path.join(cache_dir, 'cors_coord/')
    base_url = 'ftp://geodesy.noaa.gov/cors/coord/coord_08/'
    os.makedirs(cache_subdir, exist_ok=True)
    response = urllib.request.urlopen(base_url)
    file_data = response.read().decode('utf-8').split('\r\n')
    filenames = [line.split()[-1] for line in file_data if len(line) > 5 and line.endswith('coord.txt')]
    filepaths = [fetch_file(base_url, '', cache_subdir, name) for name in filenames]
    return filepaths


def fetch_cors_station_data(time, station_name, cache_dir):
    cache_subdir = os.path.join(cache_dir, 'cors_obs/')
    dt = time.as_datetime()
    folder = f"{dt.strftime('%Y/%j/')}{station_name}/"
    filename = f"{station_name}{dt.strftime('%j0.%yo')}"
    base_url = 'ftp://geodesy.noaa.gov/cors/rinex/'

    try:
        return fetch_file(base_url, folder, cache_subdir, filename, compression='.gz')
    except IOError:
        return None