from IPython.display import display, HTML

portfolio = {
    "title": "My AI App Portfolio",
    "description": "Hi! I'm a budding AI developer exploring NLP and computer vision. This portfolio showcases my hands-on projects built with Python, Gradio, and machine learning models.",
    "links": {
        "GitHub": "https://github.com/yourusername",
        "LinkedIn": "https://linkedin.com/in/yourusername"
    },
    "apps": [
        {
            "title": "Sentiment Analysis App",
            "description": "A simple NLP-based Gradio app that predicts whether a sentence is positive or negative using a logistic regression model.",
            "link": "https://d5961dc9b6a16bcd4a.gradio.live/"
        },
        {
            "title": "Coming Soon",
            "description": "Stay tuned! More AI-powered tools and apps are on the way.",
            "link": None
        }
    ]
}

# Simple text-based portfolio rendering
def display_portfolio(port):
    print("\n" + "="*40)
    print(f"🧠 {port['title']}")
    print("="*40)
    print(f"\n{port['description']}\n")

    print("🔗 Links:")
    for name, url in port['links'].items():
        print(f" - {name}: {url}")

    print("\n📦 Apps:")
    for app in port['apps']:
        print(f"\n• {app['title']}")
        print(f"  {app['description']}")
        if app['link']:
            print(f"  Launch: {app['link']}")

# Optional: Display the main app link in notebook environments
def show_main_app_link():
    main_app = portfolio['apps'][0]['link']
    if main_app:
        display(HTML(f'<a href="{main_app}" target="_blank">Click here to open the Sentiment Analysis App</a>'))

if __name__ == "__main__":
    display_portfolio(portfolio)
    show_main_app_link()
