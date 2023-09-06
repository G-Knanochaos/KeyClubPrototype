import cssutils
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from flask import render_template
import os
from main import app

def compress_css(input_file, output_file, html_file):
    with open(input_file, 'r') as infile:
        css_text = infile.read()

    parser = cssutils.CSSParser()
    stylesheet = parser.parseString(css_text)

    # Create a dictionary to store unique CSS rules
    unique_rules = {"all":{}} #each breakpoint has a dictionary of unique style:selector pairs
    kicked_selectors = {} #set eliminates duplicate kicked_selectors

    # Iterate through CSS  rules and consolidate identical ones
    for rule in stylesheet:
        if isinstance(rule, cssutils.css.CSSMediaRule): #check if rule is media rule
            #check if this media breakpoint has already been added:
            if rule.media.mediaText not in unique_rules:
                unique_rules[rule.media.mediaText] = {}

            #for each rule in this media break point
            for nested_rule in rule.cssRules:
                selector = nested_rule.selectorText
                style = nested_rule.style.cssText

                # Check if this rule already exists, if so, append selector
                if style in unique_rules[rule.media.mediaText]:
                    if selector[1:] not in kicked_selectors:
                        kicked_selectors.update({
                                selector[1:]:unique_rules[rule.media.mediaText][style]
                                #kicked_selector : og_selector
                                })
                else:
                    unique_rules[rule.media.mediaText][style] = selector
                    print(rule.media.mediaText)
        elif isinstance(rule, cssutils.css.CSSStyleRule): #check if rule is all rule
            selector = rule.selectorText
            style = rule.style

            # Check if this rule already exists, if so, append selector
            if style in unique_rules["all"]:
                if selector[1:] not in kicked_selectors:
                    kicked_selectors.update({
                            selector[1:]:unique_rules["all"][style]
                            #kicked_selector : og_selector
                            })
            else:
                unique_rules["all"][style] = selector

    # Create a new stylesheet with consolidated rules
    compressed_stylesheet = cssutils.css.CSSStyleSheet()
    for breakpoint in unique_rules:
        media_rule = cssutils.css.CSSMediaRule(mediaText = breakpoint)
        
    
        for style, selector in unique_rules[breakpoint].items():
            compressed_rule = cssutils.css.CSSStyleRule(
                                                        selectorText=selector, 
                                                        style=style)
            media_rule.add(compressed_rule)
        print(media_rule.cssText)
        compressed_stylesheet.add(media_rule)
    
    for i in range(100):
        print("filler")
    soup = None
    with open(html_file,"r") as html:
        soup = BeautifulSoup(html,'html.parser')

    print([s.attrs for s in soup if type(s) != NavigableString])
    for selector in kicked_selectors:
        '''
        with app.app_context():
            real_html = render_template(html_file)
        print(real_html)
        '''
        
        kicked_elements = soup.find_all(class_ = lambda c: c and selector in c)



        for element in kicked_elements:
            element["class"][element["class"].index(selector)] = (kicked_selectors[selector])[1:] #find og_selector of current kicked_selector

    with open(html_file,"w") as html:
        html.write(str(soup))
    print("Compress HTML saved to " +html_file)




    # Write the compressed CSS to the output file
    with open(output_file, 'w') as outfile:
        outfile.write(str(compressed_stylesheet.cssText))

#/Users/oceanhawk/Documents/Python/KeyClub Flask Setup/website/static/css/events.css
if __name__ == "__main__":

    name = "/"+input("CSS file?")
    FILE_PATH = __file__[:(-(__file__[::-1].index("/"))-1)]
    print(FILE_PATH)

    input_file = FILE_PATH + "/website/static/css" + name
    html_path =  FILE_PATH + "/website/templates" + name[:-4]  +".html"
    output_file =  input_file

    compress_css(input_file, output_file,html_path)
    print(f"Compressed CSS saved to {output_file}")