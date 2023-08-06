import time
import unittest

from requests import Request as HttpRequest

from test_data import createTestUserAgentList

from wmclient import *
from os import environ


def createTestClient():
    wmhost = environ.get("WM_HOST")
    if wmhost is None:
        wmhost = "localhost"

    wmport = environ.get("WM_PORT")
    if wmport is None:
        wmport = 8080
    else:
        wmport = int(wmport)

    return WmClient.create("http", wmhost, wmport, "")


class DetectionTask:

    def __init__(self, client, tdata, task_index):
        self.client = client
        self.test_data = tdata
        self.task_index = task_index

    def do_task(self):
        print("Starting task#: " + str(self.task_index))
        c = 0
        try:
            iterations = 5
            for i in range(iterations):
                for line in self.test_data:
                    d = self.client.lookup_useragent(line)
                    if d is None:
                        print("device is None")
                        return False
                    if not d.capabilities["wurfl_id"] == self.test_data[line]:
                        print("device wurfl does not match expected value")
                        return False
                    c += 1
                    self.client.get_all_OSes()
                    self.client.get_all_device_makes()
            print("Lines read from terminated task #" + str(self.task_index) + ": " + str(c))
            return True
        except Exception as e:
            print(e)
            return False


class WMTestUtils(object):
    def __init__(self):
        pass

    def createExpectedValueDict(self, client):
        userAgentList = createTestUserAgentList()
        dictionary = dict()
        for ua in userAgentList:
            try:
                device = client.lookup_useragent(ua)
                dictionary[ua] = device.capabilities.get("wurfl_id")
            except WmClientError as e:
                raise e
        return dictionary

    def createLookupTasks(self, tasks_count, client):
        data_dict = self.createExpectedValueDict(client)
        ltasks = []
        for i in range(tasks_count):
            tindex = i
            dt = DetectionTask(client, data_dict, tindex)
            ltasks.append(dt)
        return ltasks


class WmClientTest(unittest.TestCase):

    def test_getInfo(self):
        wmport = 8080
        swmport = environ.get("WM_PORT")
        if swmport is not None:
            wmport = int(swmport)

        client = WmClient.create("http", "localhost", wmport, "")
        info = client.get_info()
        self.assertGreater(len(info.wurfl_info), 0)
        self.assertGreater(len(info.wurfl_api_version), 0)
        self.assertGreater(len(info.wm_version), 0)
        self.assertEqual(len(info.important_headers), 7)
        self.assertGreater(len(info.wm_version), 0)
        self.assertGreater(len(info.static_capabilities), 0)
        self.assertGreater(len(info.virtual_capabilities), 0)
        client.destroy()

    def test_createWithServerDown(self):
        hasErr = False
        try:
            WmClient.create("http", "localhost", 18080, "")
        except WmClientError:
            hasErr = True
        self.assertTrue(hasErr)

    def test_createWithEmptyServerValues(self):
        hasErr = False
        try:
            WmClient.create("http", "", 0, "")
        except WmClientError:
            hasErr = True
        self.assertTrue(hasErr)

    def test_createOK(self):
        client = createTestClient()
        self.assertTrue(client)
        self.assertTrue(len(client.important_headers) > 0)
        self.assertTrue(len(client.staticCaps) > 0)
        self.assertTrue(len(client.virtualCaps) > 0)
        client.destroy()

    def test_lookupUserAgent(self):
        client = createTestClient()
        self.assertTrue(client)
        ua = "Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G950F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "SamsungBrowser/5.2 Chrome/51.0.2704.106 Mobile Safari/537.36 "
        device = client.lookup_useragent(ua)
        self.assertTrue(device)

        dcount = len(device.capabilities)
        self.assertTrue(dcount >= 13)
        self.assertEqual("true", device.capabilities["is_smartphone"])
        self.assertEqual("Smartphone", device.capabilities["form_factor"])
        self.assertEqual("SM-G950F", device.capabilities["model_name"])
        client.destroy()

    def test_lookupUserAgentWithSpecificCaps(self):

        reqCaps = {"brand_name", "model_name", "is_touchscreen", "form_factor"}
        client = createTestClient()
        client.set_requested_capabilities(reqCaps)
        ua = "Mozilla/5.0 (Nintendo Switch; WebApplet) AppleWebKit/601.6 (KHTML, like Gecko) NF/4.0.0.5.9 " \
             "NintendoBrowser/5.1.0.13341 "
        device = client.lookup_useragent(ua)
        capabilities = device.capabilities
        self.assertIsNotNone(device)
        self.assertIsNotNone(capabilities);
        self.assertEqual("Nintendo", capabilities["brand_name"])
        self.assertEqual("Switch", capabilities["model_name"])
        self.assertEqual("true", capabilities["is_touchscreen"])
        self.assertEqual(5, len(capabilities))  # 4 caps + wurfl ID
        client.destroy()

    def test_lookupUseragentEmptyUa(self):

        client = createTestClient()
        device = client.lookup_useragent("")
        self.assertIsNotNone(device)
        self.assertEqual(device.capabilities["wurfl_id"], "generic")
        client.destroy()

    def test_lookupUseragentNoneUa(self):

        client = createTestClient()
        device = client.lookup_useragent(None)
        self.assertIsNotNone(device)
        self.assertEqual(device.capabilities.get("wurfl_id"), "generic")
        client.destroy()

    def test_lookupRequestOK(self):
        client = createTestClient()
        pheaders = {
            "User-Agent": "Mozilla/5.0 (Nintendo Switch; WebApplet) AppleWebKit/601.6 (KHTML, like Gecko) "
                          "NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "X-UCBrowser-Device-UA": "Mozilla/5.0 (Nintendo Switch; ShareApplet) AppleWebKit/601.6 (KHTML, "
                                     "like Gecko) NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "Device-Stock-UA": "Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, "
                               "like Gecko) NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "Accept-Encoding": "application/json"
        }
        req = HttpRequest('GET', "http://mywebsite.com", headers=pheaders)

        device = client.lookup_request(req)
        self.assertIsNotNone(device)
        capabilities = device.capabilities
        self.assertIsNotNone(capabilities)
        self.assertTrue(len(capabilities) >= 13)
        self.assertEqual("Smart-TV", capabilities["form_factor"])
        self.assertEqual("Nintendo Switch", capabilities["complete_device_name"])
        self.assertEqual("true", capabilities["is_touchscreen"])
        self.assertEqual("nintendo_switch_ver1", capabilities["wurfl_id"])
        client.destroy()

    def test_lookupRequestOkWithSpecificCaps(self):

        client = createTestClient()
        reqCaps = {"is_mobile", "form_factor", "complete_device_name", "brand_name"}
        client.set_requested_capabilities(reqCaps)
        pheaders = {
            "User-Agent": "Mozilla/5.0 (Nintendo Switch; WebApplet) AppleWebKit/601.6 (KHTML, like Gecko) "
                          "NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "X-UCBrowser-Device-UA": "Mozilla/5.0 (Nintendo Switch; ShareApplet) AppleWebKit/601.6 (KHTML, "
                                     "like Gecko) NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "Device-Stock-UA": "Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, "
                               "like Gecko) NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "Accept-Encoding": "application/json"
        }
        req = HttpRequest('GET', "http://mywebsite.com", headers=pheaders)

        device = client.lookup_request(req)
        self.assertIsNotNone(device)
        capabilities = device.capabilities
        self.assertIsNotNone(capabilities)
        self.assertEqual(len(capabilities), 5)
        self.assertEqual("Smart-TV", capabilities["form_factor"])
        self.assertEqual("Nintendo Switch", capabilities["complete_device_name"])
        self.assertEqual("true", capabilities["is_mobile"])
        self.assertEqual("nintendo_switch_ver1", capabilities["wurfl_id"])
        print("Selected capabilities:")
        for c in capabilities:
            print(c)
        client.destroy()

    def test_lookupRequestWithSpecificCapsAndNoHeaders(self):

        client = createTestClient()
        reqCaps = {"brand_name", "model_name"}
        client.set_requested_capabilities(reqCaps)
        req = HttpRequest('GET', "http://mywebsite.com", headers={})
        device = client.lookup_request(req)
        self.assertEqual(device.capabilities.get("wurfl_id"), "generic")
        self.assertEqual(3, len(device.capabilities))
        client.destroy()

    def test_lookupWithNoneRequest(self):
        exc = False
        client = createTestClient()
        try:
            client.lookup_request(None)
        except Exception:
            exc = True
        self.assertTrue(exc)
        client.destroy()

    def test_hasStaticCapability(self):
        client = createTestClient()
        self.assertTrue(client.has_static_capability("brand_name"))
        self.assertTrue(client.has_static_capability("model_name"))
        self.assertTrue(client.has_static_capability("is_smarttv"))
        # this is a virtual capability, so it shouldn't be returned
        self.assertFalse(client.has_static_capability("is_app"))
        client.destroy()

    def test_hasVirtualCapability(self):
        client = createTestClient()
        self.assertTrue(client.has_virtual_capability("is_smartphone"))
        self.assertTrue(client.has_virtual_capability("form_factor"))
        # this is a static capability, so it shouldn't be returned
        self.assertFalse(client.has_virtual_capability("brand_name"))
        self.assertFalse(client.has_virtual_capability("is_wireless_device"))
        client.destroy()

    def test_lookupDeviceId(self):
        client = createTestClient()
        device = client.lookup_device_id("nokia_generic_series40")
        self.assertIsNotNone(device)
        capabilities = device.capabilities
        self.assertIsNotNone(capabilities)
        # num caps + num vcaps + wurfl id
        self.assertTrue(len(capabilities) >= 13)
        self.assertEqual("false", capabilities["is_smartphone"])
        self.assertEqual("Feature Phone", capabilities["form_factor"])
        client.destroy()

    def test_lookupDeviceIdWithSpecificCaps(self):
        client = createTestClient()
        reqCaps = {"brand_name", "is_smarttv"}
        reqvCaps = {"is_smartphone", "complete_device_name"}
        client.set_requested_static_capabilities(reqCaps)
        client.set_requested_virtual_capabilities(reqvCaps)
        device = client.lookup_device_id("generic_opera_mini_version1")
        self.assertIsNotNone(device)
        capabilities = device.capabilities
        self.assertIsNotNone(capabilities)
        self.assertEqual("Opera", capabilities["brand_name"])
        self.assertEqual("false", capabilities["is_smarttv"])
        self.assertEqual(5, len(capabilities))
        self.assertEqual("false", capabilities["is_smartphone"])
        self.assertEqual("Opera Mini 1", capabilities["complete_device_name"])
        client.destroy()

    def test_lookupDeviceIdWithWrongIdTest(self):

        exc = False
        errmsg = None
        client = createTestClient()
        try:
            client.lookup_device_id("nokia_generic_series40_wrong")
        except WmClientError as e:
            exc = True
            errmsg = str(e.message)
        self.assertTrue(exc)
        self.assertTrue("device is missing" in errmsg)
        client.destroy()

    def test_lookupDeviceIdWithNoneIdTest(self):

        exc = False
        errmsg = None
        client = createTestClient()
        try:
            client.lookup_device_id(None)
        except WmClientError as e:
            exc = True
            errmsg = str(e.message)
        self.assertTrue(exc)
        self.assertTrue("device is missing" in errmsg)
        client.destroy()

    def test_lookupDeviceIdWithEmptyId(self):

        exc = False
        errmsg = None
        client = createTestClient()
        try:
            client.lookup_device_id("")
        except WmClientError as e:
            exc = True
            errmsg = str(e.message)
        self.assertTrue(exc)
        self.assertTrue("device is missing" in errmsg)
        client.destroy()

    def test_lookup_headers_OK(self):
        h_client = createTestClient()
        h_client.set_cache_size(10000)
        pheaders = {
            "User-Agent": "Mozilla/5.0 (Nintendo Switch; WebApplet) AppleWebKit/601.6 (KHTML, like Gecko) "
                          "NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "X-UCBrowser-Device-UA": "Mozilla/5.0 (Nintendo Switch; ShareApplet) AppleWebKit/601.6 (KHTML, "
                                     "like Gecko) NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "Device-Stock-UA": "Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, "
                               "like Gecko) NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "Accept-Encoding": "application/json"
        }

        device = h_client.lookup_headers(pheaders)
        self.assertIsNotNone(device)
        capabilities = device.capabilities
        self.assertIsNotNone(capabilities)
        self.assertTrue(len(capabilities) >= 13)
        self.assertEqual("Nintendo Switch", capabilities["complete_device_name"])
        self.assertEqual("true", capabilities["is_touchscreen"])
        self.assertEqual("nintendo_switch_ver1", capabilities["wurfl_id"])
        self.assertEqual("Smart-TV", capabilities["form_factor"])

        cs = h_client.get_actual_cache_size()
        self.assertEqual(1, cs[1])

        # now, let's pass the same header values with mixed key case
        pheaders = {
            "User-AgEnT": "Mozilla/5.0 (Nintendo Switch; WebApplet) AppleWebKit/601.6 (KHTML, like Gecko) "
                          "NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "X-UCBrowsEr-DeVice-UA": "Mozilla/5.0 (Nintendo Switch; ShareApplet) AppleWebKit/601.6 (KHTML, "
                                     "like Gecko) NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "Device-StocK-Ua": "Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, "
                               "like Gecko) NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341",
            "Accept-EncoDing": "application/json"
        }

        device2 = h_client.lookup_headers(pheaders)
        capabilities = device2.capabilities
        self.assertIsNotNone(capabilities)
        self.assertEqual("nintendo_switch_ver1", capabilities["wurfl_id"])
        # now, despite the mixed case on header keys, we we should have a cache hit because headers
        # have been "normalized" to standard header names
        c_info = h_client.get_actual_cache_size()
        self.assertEqual(0, cs[0])
        self.assertEqual(1, cs[1])

        h_client.destroy()

    def test_lookup_headers_with_headers_none(self):
        client = createTestClient()

        try:
            client.lookup_headers(None)
        except WmClientError as e:
            self.assertTrue("headers dictionary cannot be None" in e.message)
        client.destroy()

    def test_getAllOsesTest(self):
        client = createTestClient()
        oses = client.get_all_OSes()
        self.assertIsNotNone(oses)
        self.assertTrue(len(oses) >= 30)
        client.destroy()

    def test_getAllVersionsForOSTest(self):
        client = createTestClient()
        osVersions = client.get_all_versions_for_OS("Android")
        self.assertIsNotNone(osVersions)
        self.assertTrue(len(osVersions) >= 30)
        self.assertIsNotNone(osVersions[0])
        client.destroy()

    def test_getAllDeviceMakes(self):
        client = createTestClient()
        deviceMakes = client.get_all_device_makes()
        self.assertIsNotNone(deviceMakes)
        self.assertTrue(len(deviceMakes) >= 2000)
        self.assertIsNotNone(deviceMakes[0])
        client.destroy()

    def test_getAllDevicesForMake(self):
        client = createTestClient()
        modelMktNames = client.get_all_devices_for_make("Nokia")
        self.assertIsNotNone(modelMktNames)
        self.assertTrue(len(modelMktNames) > 700)
        self.assertIsNotNone(modelMktNames[0].brand_name)
        self.assertIsNotNone(modelMktNames[5].model_name)
        client.destroy()

        for mdmk in modelMktNames:
            self.assertIsNotNone(mdmk)

    def test_getAllDevicesForMakeWithWrongMake(self):
        client = createTestClient()
        exc = False
        try:
            client.get_all_devices_for_make("Fakething")
        except WmClientError as wm:
            exc = True

            hasMsg = hasattr(wm, 'message')
            self.assertTrue(hasMsg)
            self.assertTrue("Fakething does not exist" in wm.message)
        self.assertTrue(exc)

    def test_getAllVersionsForOsWithWrongOsTest(self):
        exc = False
        try:
            client = createTestClient()
            client.get_all_devices_for_make("Fakething")
        except WmClientError as wm:
            exc = True
            hasMsg = hasattr(wm, 'message')
            self.assertTrue(hasMsg)
            self.assertTrue("Fakething does not exist" in wm.message)
        self.assertTrue(exc)

    def test_multiThreadedLookupTest(self):

        client = createTestClient()
        util = WMTestUtils()
        lookups = util.createLookupTasks(16, client)

        try:
            threads = []
            for ltask in lookups:
                t = threading.Thread(target=ltask.do_task)
                threads.append(t)
                t.start()
                print("started thread " + str(t.ident))

            for t in threads:
                t.join()
        except Exception as e:
            print("start thread error")
            self.assertIsNone(e)  # makes test fail

    def test_lru_cache_on_lookup_useragent(self):
        ua = "ZTE-Z331/1.5.0 NetFront/3.5 QTV5.1 Profile/MIDP-2.1 Configuration/CLDC-1.1"
        client = createTestClient()
        client.set_cache_size(1000)
        client.clear_caches()
        client.lookup_useragent(ua)
        cs = client.get_actual_cache_size()
        self.assertEqual(1, cs[1])
        self.assertEqual(0, cs[0])
        client.lookup_useragent(ua)

        for i in range(4):
            client.lookup_useragent(ua)
        client.lookup_useragent("fake-ua")
        cs = client.get_actual_cache_size()
        self.assertEqual(2, cs[1])
        self.assertEqual(0, cs[0])

        client.destroy()

    def test_lru_cache_on_mixed_lookups(self):
        client = createTestClient()
        client.set_cache_size(1000)
        client.clear_caches()
        ua = "ZTE-Z331/1.5.0 NetFront/3.5 QTV5.1 Profile/MIDP-2.1 Configuration/CLDC-1.1"
        client.lookup_useragent(ua)
        client.lookup_device_id("opwv_v6_generic")
        # two different lookups, only cache miss here
        cs = client.get_actual_cache_size()
        self.assertEqual(1, cs[0])
        self.assertEqual(1, cs[1])

        # 1 miss and multiple cache hit on device id
        for i in range(100):
            client.lookup_device_id("alcatel_generic_v5")
        cs = client.get_actual_cache_size()
        self.assertEqual(2, cs[0])
        for i in range(10):
            client.lookup_useragent("Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 ("
                                    "KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1")
        cs = client.get_actual_cache_size()
        self.assertEqual(2, cs[0])
        self.assertEqual(2, cs[1])

        # subtle case: ua wurfl_id passed as a user-agent
        device = client.lookup_useragent("alcatel_generic_v5")
        # this detection causes a cache miss because cache for WURFL ID and
        # http headers in general (user-agent included) are computed differently
        cs = client.get_actual_cache_size()
        self.assertEqual(2, cs[0])
        self.assertEqual(3, cs[1])
        # another subtle case, ua passed as wurfl_id.
        # In this case we don't add any element to cache because the API function raises error before
        # cache miss can be computed (cache compute is done in the decorator, after method properly returns
        try:
            client.lookup_device_id(ua)
        except Exception:
            pass
        cs = client.get_actual_cache_size()
        self.assertEqual(2, cs[0])

    # This test needs the environment variable CACHE_SIZE to be set to 1000 before starting the test session
    def test_cache_size(self):
        client = createTestClient()
        client.set_cache_size(10000)
        client.clear_caches()
        for i in range(1010):
            client.lookup_useragent("ua " + str(i))
        cs = client.get_actual_cache_size()
        self.assertEqual(1010, cs[1])
        client.destroy()

    def test_clear_lru_cache_on_set_requested_caps(self):
        client = createTestClient()
        client.set_cache_size(1000)
        client.set_requested_static_capabilities("brand_name")
        device = client.lookup_useragent("opwv_v6_generic")
        self.assertIsNotNone(device)
        cs = client.get_actual_cache_size()
        self.assertEqual(1, cs[1])
        # changing the requested capabilities causes a cache clearing invocation, because device capabilities
        # need to be re saved in order to comply with the new requirement
        client.set_requested_static_capabilities(["brand_name", "model_name"])
        cs = client.get_actual_cache_size()
        self.assertEqual(0, cs[1])

        # same test but requesting virtual capabilities only
        client.lookup_useragent("opwv_v6_generic")
        cs = client.get_actual_cache_size()
        self.assertEqual(0, cs[0])
        self.assertEqual(1, cs[1])
        client.set_requested_virtual_capabilities("form_factor")
        # again, it is reset
        cs = client.get_actual_cache_size()
        self.assertEqual(0, cs[0])
        self.assertEqual(0, cs[1])

        # same test again but requesting both static and virtual capabilities
        client.lookup_useragent("opwv_v6_generic")
        cs = client.get_actual_cache_size()
        self.assertEqual(0, cs[0])
        self.assertEqual(1, cs[1])

        client.set_requested_capabilities(["brand_name", "form_factor"])
        cs = client.get_actual_cache_size()
        self.assertEqual(0, cs[0])
        self.assertEqual(0, cs[1])
        client.destroy()

    def test_subsequent_post_get_calls(self):
        client = createTestClient()
        ua = "ZTE-Z331/1.5.0 NetFront/3.5 QTV5.1 Profile/MIDP-2.1 Configuration/CLDC-1.1"
        device = client.lookup_useragent(ua)
        self.assertIsNotNone(device)
        try:
            oses = client.get_all_OSes()
            self.assertIsNotNone(oses)
        except WmClientError as wme:
            if "response code: 405" in wme.message:
                self.fail("Subsequent calls with different methods must not produce 405 error")

    def test_set_timeout(self):
        if environ.get("SKIP_TEST") is not None:
            self.skipTest("test environment maybe faster than the shorter possible timeout")
        exc = False
        client = createTestClient()
        try:
            client.set_http_timeout(1)
            client.get_all_OSes()
        except WmClientError as e:
            if "timed out" in str(e):
                exc = True
        self.assertTrue(exc)

    def test_cache_usage(self):
        # this client has no active cache
        client = createTestClient()
        # perform detection on a dataset without using cache
        uas = createTestUserAgentList()
        start = time.time()
        for ua in uas:
            client.lookup_useragent(ua)
        tot_time_elapsed = time.time() - start
        avg_detection_time = tot_time_elapsed/len(uas)

        # now let's add a cache layer and fill it
        client.set_cache_size(10000)
        for ua in uas:
            client.lookup_useragent(ua)
        assert(client.get_actual_cache_size()[1] > 0)

        # measure cache usage times and compare it with no cache usage times
        start = time.time()
        for ua in uas:
            client.lookup_useragent(ua)
        tot_cache_time = time.time() - start
        avg_cache_time = tot_cache_time/len(uas)

        ua = "ZTE-Z331/1.5.0 NetFront/3.5 QTV5.1 Profile/MIDP-2.1 Configuration/CLDC-1.1"
        device = client.lookup_useragent(ua)
        self.assertIsNotNone(device)
        self.assertIsNotNone(device.capabilities)
        self.assertEqual("zte_z331_ver1_subuanetfront", device.capabilities["wurfl_id"])
        self.assertEqual("ZTE Z331", device.capabilities["complete_device_name"])

        # cache MUST be at least an order of magnitude faster than detection
        self.assertTrue(avg_detection_time > avg_cache_time * 10)
        self.assertTrue(tot_time_elapsed > tot_cache_time * 10)

        client.destroy()

