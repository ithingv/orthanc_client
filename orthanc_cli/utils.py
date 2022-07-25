"""
Module contains helper functions to validate and transform dicom paths and ids
"""

import xml.dom.minidom
import validators


STUDY_TAG = "0020000D"
SERIES_TAG = "0020000E"
INSTANCE_TAG = "00080018"

STUDY_ID = "study_id"
SERIES_ID = "series_id"
INSTANCE_ID = "instance_id"
FRAME_ID = "frame_id"

ID_PATH_MAP = {
    STUDY_ID : "studies",
    SERIES_ID : "series",
    INSTANCE_ID : "instances",
    FRAME_ID : "frames" 
}

SPLIT_CHAR = '/'

DICOM_XML_CONTENT_TYPE = "application/dicom+xml"


def validate_host_str(hostname):
    """
    ex)
    hostname이 올바른지 검사하는 함수
    """
    if not validators.url(hostname):
        raise ValueError('올바르지 않은 URL입니다.')
    if hostname[-1] != SPLIT_CHAR:
        hostname += SPLIT_CHAR
    return hostname


def validate_path(path):
    """
    path가 올바른지 검사하는 함수
    """
    if path:
        # path[0] == '/'
        if path[0] == SPLIT_CHAR:
            path = path[1:]
        if path[-1] == SPLIT_CHAR:
            path = path[:-1]
        path_splitted = path.split(SPLIT_CHAR)
        num_of_pieces = len(path_splitted)

        # http://localhost:8042/studies/series/intances
        if num_of_pieces < 2 or num_of_pieces % 2 \
            or path_splitted[-2] not in ['root', 'studies', 'series', 'instances', 'frames']:
            raise ValueError('올바르지 않은 경로입니다.')
    return path


def get_dicom_tag(dictionary, tag):
    """Wrapper for dicom json dict"""
    if tag not in dictionary:
        raise LookupError('{} 태그를 찾을 수 없습니다.'.format(tag))
    return dictionary[tag]["Value"][0]


def ids_from_json(json_dict):
    """
    json dictionary object에서 ids사전을 생성하는 함수
    """
    ids = {}
    ids[STUDY_ID] = get_dicom_tag(json_dict, STUDY_TAG)
    ids[SERIES_ID] = get_dicom_tag(json_dict, SERIES_TAG)
    ids[INSTANCE_ID] = get_dicom_tag(json_dict, INSTANCE_TAG)
    return ids


def get_path_level(ids):
    """Return level of path
    :params: a dict of ids study_id:<uid>:, series_id:<uid>, \
        instance_id:<uid>, [frame_id:<frame_num>]
    :returns: string level(root, studies, series, instances, frames)
    """
    if not ids:
        return "root"
    if FRAME_ID in ids:
        return ID_PATH_MAP[FRAME_ID]
    if INSTANCE_ID in ids:
        return ID_PATH_MAP[INSTANCE_ID] 
    if SERIES_ID in ids:
        return ID_PATH_MAP[SERIES_ID]
    if STUDY_ID in ids:
        return ID_PATH_MAP[STUDY_ID]
    raise ValueError("경로의 레벨을 찾을 수 없습니다.")


def ids_from_path(path):
    """path에서 study, series, instance, frame id를 parsing 하는 함수
    :param path: path to dicom object(instance or frame)
            in form of url path /studies/<uid>/series/<uid>/instances/<uid>/[/frame/<frame_num>]
    :returns: a dict of ids study_id:<uid>, series_id:<uid>, \
            instance_id:<uid>, [frame_id:<frame_num>]
    """
    path = validate_path(path)
    path_splitted = path.split(SPLIT_CHAR)
    ids = {}

    if len(path_splitted) >= 2:
        ids[STUDY_ID] = path_splitted[1]
    if len(path_splitted) >= 4:
        ids[SERIES_ID] = path_splitted[3]
    if len(path_splitted) >= 6:
        ids[INSTANCE_ID] = path_splitted[5]
    if len(path_splitted) >= 8:
        ids[FRAME_ID] = path_splitted[7]
    return ids


def path_from_ids(ids):
    """ids 딕셔너리노 부터 path 생성하는 함수
    :returns: a dict of ids study_id:<uid>, series_id:<uid>,\
              instance_id:<uid>, [frame_id:<frame_num>]
    :param path: path to dicom object(instance or frame)
             in form of url path /studies/<uid>/series/<uid>/instances/<uid>[/frames/<frame_num>]
    """
    path = ""
    
    if not ids:
        return path
    if STUDY_ID in ids:
        path += id_to_string(STUDY_ID, ids[STUDY_ID])
    if SERIES_ID in ids:
        path += id_to_string(SERIES_ID, ids[SERIES_ID])
    if INSTANCE_ID in ids:
        path += id_to_string(INSTANCE_ID, ids[INSTANCE_ID])
    if FRAME_ID in ids:
        path += id_to_string(FRAME_ID, ids[FRAME_ID])

    return path


def id_to_string(id_key, id_value):
    """id_key, id_value 값으로 문자열 생성 """
    return SPLIT_CHAR + ID_PATH_MAP[id_key] + id_value


def file_system_full_path_by_ids(ids, base_dir="./"):
    """
    ids 딕셔너리에서 file 경로 생성
    """
    path = ids[STUDY_ID] + SPLIT_CHAR + \
        ids[SERIES_ID] + SPLIT_CHAR
    if base_dir[-1] != SPLIT_CHAR:
        path = SPLIT_CHAR + path
    path = base_dir + path
    filename = ids[INSTANCE_ID]
    return path, filename


def pretty_format(body, content_type):
    """content type이 DICOM XML일 때 body 태그를 전처리하는 함수"""
    if content_type.lower() == DICOM_XML_CONTENT_TYPE:
        body = xml.dom.minidom.parseString(body).toprettyxml(indent='    ')
    return body