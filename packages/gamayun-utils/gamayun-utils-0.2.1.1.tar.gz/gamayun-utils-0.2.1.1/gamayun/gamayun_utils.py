from . import __GamayunResult_pb2_grpc as GamayunResult_pb2_grpc
from . import __GamayunResult_pb2 as GamayunResult_pb2
import grpc
import traceback
import os

def report_result_with_strings_only(results):
    job_name = __get_job_name()
    channel = grpc.insecure_channel('localhost:' + __get_port())
    stub = GamayunResult_pb2_grpc.ResultStub(channel)
    res = GamayunResult_pb2.JobResultWithRawStringsOnly(name = job_name, results = results)
    stub.ReportResultWithRawStringsOnly(res)

def report_result_with_maps_only(results):
    job_name = __get_job_name()
    channel = grpc.insecure_channel('localhost:' + __get_port())
    stub = GamayunResult_pb2_grpc.ResultStub(channel)
    wrapped_results = list()
    for elem in results:
        wrapped_results.append(GamayunResult_pb2.MapResult(mapResult = {k:v for (k,v) in elem.items() if v is not None}))
    res = GamayunResult_pb2.JobResultWithMapOnly(name = job_name, results = wrapped_results)
    stub.ReportResultWithMapOnly(res)

def report_result_with_maps_and_strings(mapResults, stringResults):
    job_name = __get_job_name()
    channel = grpc.insecure_channel("localhost:" + __get_port())
    stub = GamayunResult_pb2_grpc.ResultStub(channel)
    wrapped_results = list()
    for elem in mapResults:
        wrapped_results.append(GamayunResult_pb2.MapResult(mapResult = {k:v for (k,v) in elem.items() if v is not None}))
    res = GamayunResult_pb2.JobResultWithMapAndStrings(name = job_name, mapResults = wrapped_results, stringResults = stringResults)
    stub.ReportResultWithMapAndStrings(res)

def report_error(error):
    job_name = __get_job_name()
    channel = grpc.insecure_channel('localhost:' + __get_port())
    stub = GamayunResult_pb2_grpc.ResultStub(channel)
    err = GamayunResult_pb2.JobError(name = job_name, error = error)
    stub.ReportError(err)

def __get_job_name():
    try:
        return os.environ["GAMAYUN_JOB_NAME"]
    except:
        __report_non_job_specific_error("Cannot find GAMAYUN_JOB_NAME in environment, script cannot execute!")
        raise

def __get_port():
    return os.environ.get("GAMAYUN_GRPC_PORT", "16656")

def __report_non_job_specific_error(error):
    job_name = "Gamayun generic error"
    channel = grpc.insecure_channel('localhost:' + __get_port())
    stub = GamayunResult_pb2_grpc.ResultStub(channel)
    err = GamayunResult_pb2.JobError(name = job_name, error = error)
    stub.ReportError(err)

def run_gamayun_script_logic(callback):
    try:
        callback()
    except:
        report_error(traceback.format_exc())