# Recipe Idea Generator

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

Recipe Generator
   - Input the ingredients in our fridge, and have ChatGPT suggest different dishes
   - Add some restraints & limitations -> 30min, microwave only, no cutting, etc

Project TODOs:
- Must Features
   - User Input Text
   - ChatGPT gives 3 ~ 5 food suggestions
   - checkbox options for the restraints
- Nice to Have Features
   - User Input Pictures
   - Keep in mind: The app also needs phone support (phone screen is much smaller and narrow)
Technical things need to work on:
- ChatGPT system prompt design
- User Interface
   - User input text box
   - Show ChatGPT's response
   - Checkbox options for the restraints
      - How do we tell ChatGPT about the restraints the user has selected
      - if (knife is checked) ("knife yes")
   - User upload/take pictures

