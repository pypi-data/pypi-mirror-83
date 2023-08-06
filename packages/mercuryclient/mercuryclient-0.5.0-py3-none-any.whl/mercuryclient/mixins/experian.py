import time


class ExperianMixin:
    """
    Mixin for registering Experian requests
    """

    def request_experian_report(self, application_data, profile):
        """
        POST a request to Mercury to Request Experian report. This posts the request to
        Mercury and returns immediately. Use the returned request ID and poll
        get_experian_response to check for report.
        You can also use fetch_experian_report which is a helper function that combines
        this api and the result api to get the result.

        :param application_data: Dict containing application data to get Experian report
        :type application_data: dict
        :param profile: Experian profile name
        :type profile: str
        :return: Dict containing request ID and status
        :rtype: dict
        """
        api = "api/v1/experian/"

        application_data["profile"] = profile

        request_id, r = self._post_json_http_request(
            api, data=application_data, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:
            return {"request_id": request_id, "status": "Success"}

        raise Exception(
            "Error while sending Experian request. Status: {}, Response is {}".format(
                r.status_code, r.json()
            )
        )

    def get_experian_response(self, request_id):
        """
        Get result for Experian job request at the provided request ID. You can poll
        this method to check for response. If the job is still progressing, the status
        within the response will be IN_PROGRESS and the method can continue to be polled
        until you get either a SUCCESS or FAILURE

        :param request_id: Request ID of the Experian job request
        :type request_id: str
        :return: Dict containing request ID, status and job response within "response".
            This response will contain the "status" of the job (IN_PROGRESS, SUCCESS or
            FAILURE), a "message" and a "data" key containing a dict with the bureau
            report
        :rtype: dict
        """
        api = "api/v1/experian/"

        request_id, r = self._get_json_http_request(
            api,
            headers={"X-Mercury-Request-Id": request_id},
            send_request_id=False,
            add_bearer_token=True,
        )

        if r.status_code == 200:
            return {"request_id": request_id, "status": "Success", "response": r.json()}

        raise Exception(
            "Error while getting Experian response. Status: {}, Response is {}".format(
                r.status_code, r.json()
            )
        )

    def fetch_experian_report(
        self, application_data, profile, max_attempts=8, retry_backoff=15
    ):
        """
        Generate an Experian request and get job result

        :param application_data: Dict containing application data for Experian request
        :type application_data: dict
        :param profile: Experian profile name
        :type profile: str
        :param max_attempts: Number of attempts to make when fetching the result,
            defaults to 8
        :type max_attempts: int, optional
        :param retry_backoff: Number of seconds to backoff when retrying to get the
            result, defaults to 15
        :type retry_backoff: int, optional
        :return: Dict containing the job result
        :rtype: dict
        """

        response = self.request_experian_report(application_data, profile)

        request_id = response["request_id"]

        attempts = 0
        while attempts < max_attempts:
            time.sleep(retry_backoff)
            result = self.get_experian_response(request_id)
            if result["response"].get("status") != "IN_PROGRESS":
                return result["response"]

            retry_backoff *= 2
            attempts += 1

        raise Exception("Error while getting Experian response. Status: IN_PROGRESS")
