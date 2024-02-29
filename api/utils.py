def obj_to_student(obj):
    """
    obj의 각 속성을 serialize 해서, dict로 변환한다.
    serialize: python object --> (기본 타입) int, float, str
    :param obj: Django 모델 인스턴스
    :return: 직렬화된 사전 객체
    """
    
    student = dict(vars(obj))
    
    # 날짜 필드 직렬화
    if obj.birthdate:
        student['birthdate'] = obj.birthdate.isoformat()
    else:
        student['birthdate'] = '9999-12-31'

    del student['_state']
    return student


def obj_to_test(obj):
    """
    obj의 각 속성을 serialize 해서, dict로 변환한다.
    serialize: python object --> (기본 타입) int, float, str
    :param obj: Django 모델 인스턴스
    :return: 직렬화된 사전 객체
    """
    
    test = dict(vars(obj))

    # ManyToMany 필드 직렬화
    if obj.student:
        test['student'] = [t.name for t in obj.student.all()]
    else:
        test['student'] = []

    # 날짜 필드 (auto_now_add=True) 직렬화
    if obj.test_date:
        test['test_date'] = obj.test_date.isoformat()
    else:
        test['test_date'] = None

    # 날짜시간 필드 직렬화
    if obj.consulting_schedule:
        test['consulting_schedule'] = obj.consulting_schedule.isoformat()
    else:
        test['consulting_schedule'] = None

    test['consulting_status'] = bool(obj.consulting_status)
        
    del test['_state']
    return test
