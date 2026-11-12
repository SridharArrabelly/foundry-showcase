from observed_tools import successful_business_tools


def test_requires_matching_successful_execution_not_a_tool_name_in_prose():
    call = {"type": "function_call", "name": "volt-business-tools___getRecallNotices",
            "status": "completed", "call_id": "actual-call"}
    result = {"type": "function_call_output", "status": "completed",
              "call_id": "actual-call", "output": '{"synthetic":true,"status":"needs_batch"}'}
    assert successful_business_tools({"output": [call, result]}) == [call["name"]]
    assert successful_business_tools({"output": [call]}) == []
    assert successful_business_tools({"output": [call, {**result, "call_id": "different"}]}) == []
    assert successful_business_tools({"output": [{"type": "message", "text": call["name"]}]}) == []


def test_success_shaped_transport_error_does_not_count_as_business_evidence():
    call = {"type": "function_call", "name": "volt-business-tools___getOrderStatus",
            "status": "completed", "call_id": "actual-call"}
    result = {"type": "function_call_output", "status": "completed",
              "call_id": "actual-call", "output": '{"error":"invalid_arguments"}'}
    assert successful_business_tools({"output": [call, result]}) == []
