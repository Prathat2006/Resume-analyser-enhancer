from llminit import LLMManager

manager = LLMManager()
llm_instance=manager.setup_llm_with_fallback()


prompt = "you are hr you check job requirements from jobs json and user resume from user json and give score on the basiss of how much the resume is "


result=manager.invoke_with_fallback(
    llm_instance,
    manager.DEFAULT_FALLBACK_ORDER,
    prompt)

print(result)