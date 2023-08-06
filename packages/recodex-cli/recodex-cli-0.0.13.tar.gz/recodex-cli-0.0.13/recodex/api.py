import requests
from json import JSONDecodeError
import logging


class ApiClient:
    def __init__(self, api_url=None, api_token=None):
        self.api_url = api_url
        self.headers = {}

        if api_token is not None:
            self.headers["Authorization"] = "Bearer " + api_token

    # Internal

    def call(self, method, url, files={}, data={}, stream=False):
        if self.api_url is None:
            raise RuntimeError("The API URL is not configured")

        return requests.request(method, self.api_url + "/v1/" + url, files=files, json=data, headers=self.headers, stream=stream)

    def post(self, url, files={}, data={}):
        return self.extract_payload(self.call("post", url, files, data))

    def get(self, url):
        return self.extract_payload(self.call("get", url))

    def download(self, url, file_name):
        try:
            r = self.call("get", url, stream=True)
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:   # filter out keep-alive new chunks
                        f.write(chunk)
        except Exception:
            logging.error("Downloading file {} failed ...".format(url))
            raise RuntimeError("Downloading file failed")

    def delete(self, url):
        return self.extract_payload(self.call("delete", url))

    def get_status(self):
        return self.call("get", "").json()

    # Exercises and related stuff

    def get_runtime_environments(self):
        return self.get("/runtime-environments")

    def get_pipelines(self):
        return self.get("/pipelines")

    def get_exercise(self, exercise_id):
        return self.get("/exercises/{}".format(exercise_id))

    def get_exercises(self, offset=0, limit=0):
        return self.get("/exercises?offset={}&limit={}".format(offset, limit))["items"]

    def get_reference_solutions(self, exercise_id):
        return self.get("/reference-solutions/exercise/{}".format(exercise_id))

    def get_reference_solution_evaluations(self, solution_id):
        return self.get("/reference-solutions/{}/evaluations".format(solution_id))

    def upload_file(self, filename, stream):
        return self.post("/uploaded-files", files={"file": (filename, stream)})

    def get_uploaded_file_data(self, file_id):
        return self.get("/uploaded-files/{}".format(file_id))

    def create_exercise(self, group_id):
        return self.post("/exercises", data={
            "groupId": group_id
        })

    def add_exercise_attachments(self, exercise_id, file_ids):
        self.post("/exercises/{}/attachment-files".format(exercise_id), data={"files": file_ids})

    def get_exercise_attachments(self, exercise_id):
        return self.get("/exercises/{}/attachment-files".format(exercise_id))

    def add_exercise_files(self, exercise_id, file_ids):
        self.post("/exercises/{}/supplementary-files".format(exercise_id), data={"files": file_ids})

    def get_exercise_files(self, exercise_id):
        return self.get("/exercises/{}/supplementary-files".format(exercise_id))

    def set_exercise_score_config(self, exercise_id, score_config: str):
        return self.post("/exercises/{}/score-config".format(exercise_id), data={"scoreConfig": score_config})

    def update_exercise(self, exercise_id, details):
        self.post('/exercises/{}'.format(exercise_id), data=details)

    def delete_exercise(self, exercise_id):
        self.delete('/exercises/{}'.format(exercise_id))

    def delete_reference_solution_evaluation(self, evaluation_id):
        self.delete('/reference-solutions/evaluation/{}'.format(evaluation_id))

    def create_reference_solution(self, exercise_id, data):
        return self.post('/reference-solutions/exercise/{}/submit'.format(exercise_id), data=data)

    def update_environment_configs(self, exercise_id, configs):
        self.post("/exercises/{}/environment-configs".format(exercise_id), data={
            "environmentConfigs": configs
        })

    def get_exercise_config(self, exercise_id):
        return self.get("/exercises/{}/config".format(exercise_id))

    def update_exercise_config(self, exercise_id, config):
        self.post("/exercises/{}/config".format(exercise_id), data={"config": config})

    def set_exercise_tests(self, exercise_id, tests):
        self.post("/exercises/{}/tests".format(exercise_id), data={"tests": tests})

    def get_exercise_tests(self, exercise_id):
        return self.get("/exercises/{}/tests".format(exercise_id))

    def update_limits(self, exercise_id, environment_id, hwgroup_id, limits):
        self.post("/exercises/{}/environment/{}/hwgroup/{}/limits".format(exercise_id, environment_id, hwgroup_id),
                  data={"limits": limits})

    def evaluate_reference_solutions(self, exercise_id):
        self.post("/reference-solutions/exercise/{}/evaluate".format(exercise_id), data={})

    def resubmit_reference_solution(self, ref_solution_id, debug=False):
        return self.post("/reference-solutions/{}/resubmit".format(ref_solution_id), data={"debug": debug})

    def get_hwgroups(self):
        return self.get("/hardware-groups")

    def get_exercise_tags(self):
        return self.get("/exercises/tags")

    def get_exercise_tags_stats(self):
        return self.get("/exercises/tags-stats")

    def exercise_add_tag(self, exercise_id, tag):
        return self.post("/exercises/{}/tags/{}".format(exercise_id, tag))

    def exercise_remove_tag(self, exercise_id, tag):
        return self.delete("/exercises/{}/tags/{}".format(exercise_id, tag))

    def exercise_tags_rename_global(self, tag, rename_to, force):
        return self.post("/exercises/tags/{}?renameTo={}&force={}".format(tag, rename_to, 1 if force else 0))

    def exercise_tags_remove_global(self, tag):
        return self.delete("/exercises/tags/{}".format(tag))

    # Authentication

    def login(self, username, password):
        return self.post("/login", data={
            "username": username,
            "password": password
        })

    def login_external(self, service_id, auth_type, credentials):
        return self.post("/login/{}/{}".format(service_id, auth_type), data=credentials)

    def takeover(self, user_id):
        return self.post("/login/takeover/{}".format(user_id))

    def refresh_token(self):
        return self.post("/login/refresh")["accessToken"]

    # Users

    def get_user(self, user_id):
        return self.get("/users/{}".format(user_id))

    def update_user(self, user_id, user_data):
        return self.post("/users/{}".format(user_id), data=user_data)

    def search_users(self, instance_id, search_string):
        return self.get("/users/?filters[instanceId]={}&filters[search]={}".format(instance_id, search_string))["items"]

    def register_user(self, instance_id, email, first_name, last_name, password):
        return self.post("/users", data={
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'password': password,
            'passwordConfirm': password,
            'instanceId': instance_id
        })

    def delete_user(self, user_id):
        return self.delete("/users/{}".format(user_id))

    def set_allow_user(self, user_id, allow):
        return self.post("/users/{}/allowed".format(user_id), data={"isAllowed": allow})

    # Groups

    def group_add_student(self, group_id, user_id):
        return self.post("/groups/{}/students/{}".format(group_id, user_id))

    def group_remove_student(self, group_id, user_id):
        return self.delete("/groups/{}/students/{}".format(group_id, user_id))

    def group_attach_exercise(self, group_id, exercise_id):
        return self.post("/exercises/{}/groups/{}".format(exercise_id, group_id))

    def group_detach_exercise(self, group_id, exercise_id):
        return self.delete("/exercises/{}/groups/{}".format(exercise_id, group_id))

    # Assignments and related stuff...

    def get_assignment(self, assignment_id):
        return self.get("/exercise-assignments/{}".format(assignment_id))

    def get_assignment_solutions(self, assignment_id):
        return self.get("/exercise-assignments/{}/solutions".format(assignment_id))

    def get_assignment_best_solutions(self, assignment_id):
        return self.get("/exercise-assignments/{}/best-solutions".format(assignment_id))

    def get_solution_comments(self, solution_id):
        return self.get("/comments/{}".format(solution_id))

    def solution_set_bonus_points(self, solution_id, bonus_points, override):
        return self.post("assignment-solutions/{}/bonus-points".format(solution_id), data={"overriddenPoints": override, "bonusPoints": bonus_points})

    def solution_set_flag(self, solution_id, flag, value):
        return self.post("assignment-solutions/{}/set-flag/{}".format(solution_id, flag), data={"value": value})

    def solution_resubmit(self, solution_id, debug=False):
        return self.post("assignment-solutions/{}/resubmit".format(solution_id), data={"debug": debug})

    def delete_solution(self, solution_id):
        return self.delete("assignment-solutions/{}".format(solution_id))

    # Shadow Assignments

    def get_shadow_assignment(self, assignment_id):
        return self.get("/shadow-assignments/{}".format(assignment_id))

    def create_shadow_assignment_points(self, assignment_id, user_id, points, note, awarded_at=None):
        return self.post("/shadow-assignments/{}/create-points/".format(assignment_id), data={
            'userId': user_id,
            'points': points,
            'note': note,
            'awardedAt': awarded_at,
        })

    def update_shadow_assignment_points(self, points_id, points, note, awarded_at=None):
        return self.post("/shadow-assignments/points/{}".format(points_id), data={
            'points': points,
            'note': note,
            'awardedAt': awarded_at,
        })

    def delete_shadow_assignment_points(self, points_id):
        return self.delete("/shadow-assignments/points/{}".format(points_id))

    # Misc

    def get_group_students(self, group_id):
        return self.get("/groups/{}/students".format(group_id))

    def get_user_solutions(self, assignment_id, user_id):
        return self.get("/exercise-assignments/{}/users/{}/solutions".format(assignment_id, user_id))

    def download_solution(self, solution_id, file_name):
        return self.download("/assignment-solutions/{}/download-solution".format(solution_id), file_name)

    @staticmethod
    def extract_payload(response):
        try:
            json = response.json()
        except JSONDecodeError:
            logging.error("Loading JSON response failed, see full response below:")
            logging.error(response.text)
            raise RuntimeError("Loading JSON response failed")

        if not json["success"]:
            raise RuntimeError("Received error from API: " + json["error"]["message"])

        return json["payload"]
