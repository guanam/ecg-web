# 在 views.py 中
import base64

from django.http import HttpResponseRedirect
from django.contrib import messages
from matplotlib import pyplot as plt

from .models import PatientManage
from .model.xresnet1d import ecg_inference
import pandas as pd
import torch
import numpy as np
from django.http import HttpResponse
from io import BytesIO
from django.http import JsonResponse




def run_prediction_view(request, patient_id):
    try:
        patient = PatientManage.objects.get(pk=patient_id)
        input = patient.patient_ecg
        file_extension = input.name.split('.')[-1]
        if file_extension.lower() == 'csv':
            data = np.loadtxt(input, delimiter=",")
        elif file_extension.lower() == 'txt':
            data = np.loadtxt(input, delimiter="\t")
        else:
            messages.error(request, 'Unsupported file type.')
            return

        input_ecg = torch.from_numpy(data).float().unsqueeze(0)
        lead, prediction_result = ecg_inference(input_ecg)
        patient.diagnosis_result = prediction_result
        patient.save()
        result_message = f'诊断完成! {lead}导联诊断结果为: {prediction_result}'
        messages.success(request, result_message)
    except PatientManage.DoesNotExist:
        messages.error(request, '病人不存在!')
    except Exception as e:
        messages.error(request, '预测过程中出现错误: {}'.format(e))

    # 返回到原来的 admin 页面
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def generate_ecg_plot(request, patient_id):

    patient = PatientManage.objects.get(pk=patient_id)
    input = patient.patient_ecg
    file_extension = input.name.split('.')[-1]
    if file_extension.lower() == 'csv':
        data = np.loadtxt(input, delimiter=",")
    elif file_extension.lower() == 'txt':
        data = np.loadtxt(input, delimiter="\t")

    plt.rcParams['figure.figsize'] = (20.0, 10.0)
    plt.figure()
    plt.plot(data[0], linewidth=1.2)
    plt.grid(linestyle='--')
    if patient.diagnosis_result is not None:
        plt.title(patient.diagnosis_result)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # base64_image = base64.b64encode(image_png).decode('utf-8')
    # return JsonResponse({'image_data': base64_image})

    return HttpResponse(image_png, content_type='image/png')


