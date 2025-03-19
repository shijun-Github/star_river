from langchain_openai import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Define a system prompt that tells the model how to use the retrieved context
system_prompt = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.
Context: {context}:"""

# Define a question
question = """What are the main components of an LLM-powered autonomous agent system?"""

# Retrieve relevant documents
vectorstore = MyVectorStore()
retriever = vectorstore.as_retriever()
docs = retriever.invoke(question)

# Combine the documents into a single string
docs_text = "".join(d.page_content for d in docs)

# Populate the system prompt with the retrieved context
system_prompt_fmt = system_prompt.format(context=docs_text)

# Create a model
model = ChatOpenAI(model="gpt-4o", temperature=0)

# Generate a response
questions = model.invoke([SystemMessage(content=system_prompt_fmt),
                          HumanMessage(content=question)])


def execute(self, model_id, system, prompt, dialogue_number, history_chat_record, stream, chat_id, chat_record_id,
            model_params_setting=None, dialogue_type=None, model_setting=None, **kwargs) -> NodeResult:
    if dialogue_type isNone:
        dialogue_type = 'WORKFLOW'
    if model_params_setting isNone:
        model_params_setting = get_default_model_params_setting(model_id)
        if model_setting isNone:
            model_setting = {
                'reasoning_content_enable': False,
                'reasoning_content_end': '</think>',
                'reasoning_content_start': '<think>'           }
            self.context['model_setting'] = model_setting       # 获取 LLM 模型实例，底层借助 LangChain 封装
            chat_model = get_model_instance_by_model_user_id(model_id, self.flow_params_serializer.data.get('user_id'), **model_params_setting)       # 构建历史消息
            history_message = self.get_history_message(history_chat_record, dialogue_number, dialogue_type, self.runtime_node_id)
            self.context['history_message'] = history_message       # 生成当前问题的提示信息
            question = self.generate_prompt_question(prompt)
            self.context['question'] = question.content
            system = self.workflow_manage.generate_prompt(system)
            self.context['system'] = system       # 构造最终交互的消息列表，利用 LangChain 中的消息类型进行封装
            message_list = self.generate_message_list(system, prompt, history_message)
            self.context['message_list'] = message_list
            if stream:
                response = chat_model.stream(message_list)
                return NodeResult({
                    'result': response,
                    'chat_model': chat_model,
                    'message_list': message_list,
                    'history_message': history_message,
                    'question': question.content
                }, {}, _write_context=write_context_stream)
            else:
                response = chat_model.invoke(message_list)
                return NodeResult({
                    'result': response,
                    'chat_model': chat_model,
                    'message_list': message_list,
                    'history_message': history_message,
                    'question': question.content
                }, {}, _write_context=write_context)


def execute(self, dataset_id_list, dataset_setting, question, exclude_paragraph_id_list=None, **kwargs) -> NodeResult:
    self.context['question'] = question
    if len(dataset_id_list) == 0:
        return get_none_result(question)       # 根据知识库列表，获取统一的嵌入模型ID
    model_id = get_embedding_id(dataset_id_list)       # 获取嵌入模型实例，基于 LangChain 调用嵌入接口
    embedding_model = get_model_instance_by_model_user_id(model_id, self.flow_params_serializer.data.get('user_id'))       # 将问题转换为向量
    embedding_value = embedding_model.embed_query(question)  # 获取向量数据库实例，此处基于 PG Vector 封装
    vector = VectorStore.get_embedding_vector()
    exclude_document_id_list = [str(document.id) for document in QuerySet(Document).filter(dataset_id__in=dataset_id_list, is_active=False)]       # 调用向量检索接口，根据向量距离返回相似候选文档
    embedding_list = vector.query(
        question, embedding_value, dataset_id_list, exclude_document_id_list,
        exclude_paragraph_id_list, True, dataset_setting.get('top_n'),
        dataset_setting.get('similarity'), SearchMode(dataset_setting.get('search_mode')))       # 手动关闭数据库连接
    connection.close()
    if embedding_list isNone:
        return get_none_result(question)
    paragraph_list = self.list_paragraph(embedding_list, vector)
    result = [self.reset_paragraph(paragraph, embedding_list) for paragraph in paragraph_list]
    result = sorted(result, key=lambda p: p.get('similarity'), reverse=True)
    return NodeResult({'result': result, 'question': question}, {})



"""
word
https://blog.csdn.net/2201_75600005/article/details/145556848
https://zhuanlan.zhihu.com/p/27464156624


video
https://www.bilibili.com/video/BV1mrkjYMEST/?spm_id_from=333.337.search-card.all.click&vd_source=20d99e8be4a2835522fb1df2ad8af672
"""