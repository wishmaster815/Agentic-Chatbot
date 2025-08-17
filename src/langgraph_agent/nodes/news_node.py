from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate

class ai_news_node:
    def __init__(self, llm, tavily_api_key=None):
        # Pass API key explicitly or ensure it's set in env
        self.tavily = TavilySearch(api_key=tavily_api_key)
        self.llm = llm
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI news based on the specified frequency.
        """
        frequency = state['messages'][0].content.lower().strip()
        self.state['frequency'] = frequency

        time_range_map = {'daily': 'day', 'weekly': 'week', 'monthly': 'month', 'year': 'year'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 366}

        response = self.tavily.invoke({
            "query": "Top Artificial Intelligence (AI) technology news India and globally",
            "topic": "news",
            "time_range": time_range_map.get(frequency, 'day'),   # ✅ safe default
            "include_answer": "advanced",
            "max_results": 20,
            "days": days_map.get(frequency, 1),
            # "include_domains": ["techcrunch.com", "venturebeat.com/ai"]
        })

        state['news_data'] = response.get("results", [])
        self.state['news_data'] = state['news_data']
        return state
    
    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM.
        """
        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", 
            """Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))

        # ✅ Clean up any invalid characters before saving
        summary = response.content.encode("utf-8", errors="ignore").decode("utf-8")

        state['summary'] = summary
        self.state['summary'] = summary
        return self.state
    
    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"

        # ✅ Always write with utf-8, ignore bad chars
        with open(filename, 'w', encoding="utf-8", errors="ignore") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)

        self.state['filename'] = filename
        return self.state
