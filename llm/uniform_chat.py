import os

from openai import OpenAI


class UniformChat:
    """
    A simple wrapper class for calling the Uniform AI model.
    include openai, kimi, deepSeek, doubao, claude, local, etc.
    """
    def __init__(self,
                 api_type='local',
                 base_url: str | None = None,
                 api_key: str | None = None,
                 model="",
                 system_message="You are a helpful assistant",
                 temperature=0.8,
                 top_p=0.8,
                 max_tokens=4096):

        self.api_type = api_type
        if self.api_type == 'local':
            self.base_url = "http://localhost:8000/v1"
            self.api_key = "EMPTY"
            if model:
                self.model = model
            else:
                self.model = "Qwen/Qwen2.5-7B-Instruct"

        elif self.api_type == 'custom':
            # OpenAI-compatible custom endpoint.
            # Priority: init args > env > (api_key fallback to "EMPTY")
            self.base_url = base_url or os.getenv("CUSTOM_BASE_URL")
            self.api_key = api_key or os.getenv("CUSTOM_API_KEY")
            if not self.base_url:
                raise ValueError(
                    "api_type='custom' 需要提供 base_url（构造参数 base_url=... 或环境变量 CUSTOM_BASE_URL）"
                )
            if model:
                self.model = model
            else:
                self.model = "gpt-4o-mini"

        elif self.api_type == 'openai':
            self.base_url = "https://api.openai.com/v1"
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if model:
                self.model = model
            else:
                self.model = "gpt-4o-mini"

        elif self.api_type == 'kimi':
            self.base_url = "https://api.moonshot.cn/v1"
            self.api_key = api_key or os.getenv("KIMI_API_KEY")
            if model:
                self.model = model
            else:
                self.model = "moonshot-v1-8k"

        elif self.api_type == 'deepseek':
            self.base_url = "https://ark.cn-beijing.volces.com/api/v3/"
            self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
            if model:
                self.model = model
            else:
                self.model = "deepseek-v3-241226"

        elif self.api_type == 'doubao':
            self.base_url = "https://ark.cn-beijing.volces.com/api/v3/"
            self.api_key = api_key or os.getenv("DOUBAO_API_KEY")
            if model:
                self.model = model
            else:
                self.model = "doubao-1.5-pro-32k-250115"
        elif self.api_type == 'claude':
            # Anthropic Claude uses its own SDK (not OpenAI-compatible).
            # API key default env: ANTHROPIC_API_KEY
            self.base_url = None
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if model:
                self.model = model
            else:
                self.model = "claude-sonnet-4-0"
        else:
            raise ValueError(f"Invalid API type: {self.api_type}")

        # Initialize client
        if self.api_type == "claude":
            try:
                import anthropic  # type: ignore
            except Exception as e:
                raise ImportError(
                    "使用 api_type='claude' 需要安装 anthropic SDK：pip install anthropic，并设置环境变量 ANTHROPIC_API_KEY"
                ) from e

            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            # OpenAI-compatible clients (openai/kimi/deepseek/doubao/local)
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )
        self.system_message = system_message
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

        print(f"Initialized {self.api_type} client with model {self.model}")

    def list_models(self):
        """
        列出当前 api_type 对应 endpoint 可用的模型列表。

        Returns:
            list[str]: 模型 id 列表（尽力而为；不支持/失败则返回空列表）
        """
        try:
            if self.api_type == "claude":
                models_attr = getattr(self.client, "models", None)
                if models_attr is None:
                    return []
                list_fn = getattr(models_attr, "list", None)
                if list_fn is None:
                    return []
                resp = list_fn()
                data = getattr(resp, "data", None) or []
                ids = []
                for item in data:
                    mid = getattr(item, "id", None)
                    if mid:
                        ids.append(mid)
                return ids

            resp = self.client.models.list()
            data = getattr(resp, "data", None) or []
            ids = []
            for item in data:
                mid = getattr(item, "id", None)
                if mid:
                    ids.append(mid)
            return ids
        except Exception as e:
            print("Error listing %s models, Exception Info: %s: %s, %s, %s" % (self.api_type, e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, type(e), e))
            return []

    def _should_avoid_temperature_and_top_p_together(self) -> bool:
        """
        一些提供商/路由（尤其是 Anthropic/Claude）不允许同时指定 temperature 和 top_p。
        这里做一个尽力而为的检测，避免 400 invalid_request_error。
        """
        m = (self.model or "").lower()
        # OpenAI-compatible 路由里常见的 Anthropic 命名：anthropic/claude-...
        if m.startswith("anthropic/"):
            return True
        # 兼容可能直接传 claude-xxx 的情况
        if m.startswith("claude"):
            return True
        return self.api_type == "claude"

    def _sampling_kwargs(self) -> dict:
        """
        统一生成采样参数，必要时避免 temperature 与 top_p 同时出现。
        默认策略：若两者都存在且不兼容，则保留 temperature，移除 top_p。
        """
        kwargs: dict = {}
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if self.top_p is not None:
            kwargs["top_p"] = self.top_p

        if self._should_avoid_temperature_and_top_p_together():
            if "temperature" in kwargs and "top_p" in kwargs:
                kwargs.pop("top_p", None)
        return kwargs

    def get_response(self,
                     user_message):
        """
        Get a response from the Uniform AI model.

        Args:
            user_message (str): The user's message/prompt

        Returns:
            str: The model's response
        """
        try:
            if self.api_type == "claude":
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=self.system_message,
                    messages=[{"role": "user", "content": user_message}],
                    **self._sampling_kwargs(),
                )
                # Anthropic returns a list of content blocks; keep behavior consistent by returning text.
                return "".join(
                    block.text for block in getattr(message, "content", []) if getattr(block, "type", None) == "text"
                ).strip()
            else:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_message},
                        {"role": "user", "content": user_message},
                    ],
                    **self._sampling_kwargs(),
                    max_tokens=self.max_tokens,
                )
                return completion.choices[0].message.content

        except Exception as e:
            print("Error calling %s API, Exception Info: %s: %s, %s, %s" % (self.api_type, e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, type(e), e))

            # 抛出异常，让调用者处理
            raise e

    def get_response_stream(self,
                            user_message):
        """
        Get a response from the Uniform AI model.

        Args:
            user_message (str): The user's message/prompt

        Returns:
            str: The model's response
        """
        try:
            if self.api_type == "claude":
                # Anthropic streaming API yields incremental text deltas.
                with self.client.messages.stream(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=self.system_message,
                    messages=[{"role": "user", "content": user_message}],
                    **self._sampling_kwargs(),
                ) as stream:
                    for text in stream.text_stream:
                        if text:
                            yield text
            else:
                chunks = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_message},
                        {"role": "user", "content": user_message},
                    ],
                    **self._sampling_kwargs(),
                    max_tokens=self.max_tokens,
                    stream=True
                )
                for chunk in chunks:
                    if not chunk.choices:
                        continue
                    elif chunk.choices[0].finish_reason == "stop":
                        break
                    else:
                        yield chunk.choices[0].delta.content

        except Exception as e:
            print("Error calling %s API, Exception Info: %s: %s, %s, %s" % (self.api_type, e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, type(e), e))

            # 抛出异常，让调用者处理
            raise e

    def tenacity_chat(self,
                     user_message):
        """
        带重试机制的聊天方法，如果失败会尝试三次，都失败则 fallback 到 OpenAI。

        Args:
            user_message (str): 用户消息

        Returns:
            str: 模型的响应
        """
        max_retries = 3
        current_retry = 0

        while current_retry < max_retries:
            try:
                return self.get_response(
                    user_message=user_message
                )

            except Exception as e:
                current_retry += 1
                print(f"尝试 {current_retry}/{max_retries} 失败: {str(e)}")

                if current_retry == max_retries:
                    print("所有重试都失败，切换到 OpenAI...")

                    # 创建 OpenAI 实例作为 fallback
                    fallback_chat = UniformChat(
                        api_type='openai',
                        system_message=self.system_message
                    )

                    return fallback_chat.get_response(
                        user_message=user_message
                    )

    def tenacity_chat_stream(self,
                            user_message):
        """
        带重试机制的流式聊天方法，如果失败会尝试三次，都失败则 fallback 到 OpenAI。

        Args:
            user_message (str): 用户消息

        Yields:
            str: 模型的流式响应
        """
        max_retries = 3
        current_retry = 0

        while current_retry < max_retries:
            try:
                for chunk in self.get_response_stream(
                    user_message=user_message
                ):
                    yield chunk

                return  # 如果成功完成，直接返回

            except Exception as e:
                current_retry += 1
                print(f"尝试 {current_retry}/{max_retries} 失败: {str(e)}")

                if current_retry == max_retries:
                    print("所有重试都失败，切换到 OpenAI...")

                    # 创建 OpenAI 实例作为 fallback
                    fallback_chat = UniformChat(
                        api_type='openai',
                        system_message=self.system_message
                    )

                    for chunk in fallback_chat.get_response_stream(
                        user_message=user_message
                    ):
                        yield chunk

                    return


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    # api_type = 'local'
    # api_type = 'openai'
    api_type = 'kimi'
    # api_type = 'deepseek'
    # api_type = 'doubao'
    # api_type = 'claude'
    # api_type = 'custom'


    chat = UniformChat(
        api_type=api_type,
        # base_url="",  # for custom api_type
        # model="anthropic/claude-opus-4-6",
        system_message="你是一个专业的金融分析师，擅长分析金融数据和市场趋势。"
    )

    print('-' * 50, 'list models', '-' * 50)
    print(chat.list_models())
    print('\n')

    # non-stream
    print('-' * 50, 'non-stream mode', '-' * 50)
    response = chat.get_response("你是谁")
    print(response)
    print('\n')

    # stream
    print('-' * 50, 'stream mode', '-' * 50)
    response = chat.get_response_stream("你是谁")
    for chunk in response:
        print(chunk, end="", flush=True)
    print('\n\n')


    # tenacity non-stream
    print('-' * 50, 'tenacity non-stream mode', '-' * 50)
    response = chat.tenacity_chat("你是谁")
    print(response)
    print('\n')

    # tenacity stream
    print('-' * 50, 'tenacity stream mode', '-' * 50)
    response = chat.tenacity_chat_stream("你是谁")
    for chunk in response:
        print(chunk, end="", flush=True)
    print('\n\n')
