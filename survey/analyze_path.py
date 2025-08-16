def analyze_path(survey):
    s1 = survey.step1
    s2 = survey.step2
    s3 = survey.step3
    s4 = survey.step4
    s5 = survey.step5
    s6 = survey.step6

    # تحلیل نمونه:
    if 'ai' in s1.get('interests', []):
        return {
            'mainPath': 'ai',
            'suggestions': ['web', 'data'],
            'summary': 'شما علاقه به AI دارید و مسیر مناسبی است.'
        }

    return {
        'mainPath': 'web',
        'suggestions': ['ai', 'game'],
        'summary': 'مسیر پیشنهادی: توسعه وب'
    }
