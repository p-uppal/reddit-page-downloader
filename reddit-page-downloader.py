import praw

from fpdf import FPDF

from datetime import datetime

import unicodedata

#def unicode_normalize(s):
#    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

reddit = praw.Reddit("bot1",config_interpolation="basic")


url = input("Enter the URL: ")

#Hard Coded Parameters (deprecated for now):
tree_depth = 20
tree_breadth = 40


submission = reddit.submission(url=url)
submission.comments.replace_more(limit=1)

author = submission.author
title = submission.title
is_self = submission.is_self
permalink = submission.permalink
selftext = submission.selftext
subreddit = submission.subreddit

top_level_comments = list(submission.comments)
 

class PDF(FPDF):

    def lines(self):
        self.set_line_width(0.1)
        self.line(0,pdf_h/2,210,pdf_h/2)

    def print_title(self,text=title):
        self.set_font('VerdanaB', '', 16)
        self.multi_cell(0, 7, align='L', txt=text, border=0,ln=1)

    def print_line(self,selftext,font_size=10,border_size=0):
        self.set_x(15.0)
        self.set_font('Verdana', '', font_size)
        self.multi_cell(0,5,selftext,align='L',border=border_size,ln=1)

    def print_para(self,selftext,font_size=10,border_size=0):
        self.set_x(25.0)
        self.set_font('Verdana', '', font_size)
        self.multi_cell(160,5,selftext,align='L',border=border_size, ln=1)

    def print_text(self,text,level,border_size=0):
        #text = text.encode('cp1252','strict')
        #text = unicode_normalize(text.decode())
        text2 = text.encode('latin-1', 'replace').decode('latin-1')
        curr = self.get_x()
        indent = {
        0: 25,
        1: 35,
        2: 45,
        3: 55,
        4: 65,
        5: 75,
        6: 85,
        7: 95,
        8: 105,
        9: 115,
        10: 125,
        11: 135,
        12: 145,
        13: 155,
        14: 165,
        15: 175,
        16: 185,
        17: 195,
        18: 205,
        19: 215,
        20: 225,
        21: 235,
        22: 245,
        23: 255,
        24: 265,
        25: 275
        }

        #print(indent.get(level))
        self.set_x(float(indent.get(level)))

        self.set_font('Verdana', '', 10)
        self.multi_cell(0,5,text2,align='L',border=border_size,ln=1)
        self.set_x(curr)


pdf = PDF()
pdf.add_page()
pdf.set_doc_option('core_fonts_encoding', 'utf-8')
pdf.set_xy(15.0,5.0)
pdf.add_font('Verdana', '', "C:\\Windows\\Fonts\\verdana.ttf", uni=True)
pdf.add_font('VerdanaB', '', "C:\\Windows\\Fonts\\verdana.ttf", uni=True)
pdf.set_font('Verdana', '', 14)

pdf.print_line("https://www.reddit.com" + permalink + "\n",6)

pdf.set_xy(15.0,10.0)

#pdf.set_font('Arial', 'B', 14)
#pdf.set_doc_option("core_fonts_encoding",windows-1252)
#pdf_w=210
#pdf_h=297

pdf.print_title()

pdf.print_line("/u/" + submission.author.name + "  " + str(submission.score) + " points  [" + str(datetime.fromtimestamp(submission.created_utc)) + "]",10)
#pdf.ln(7)
if is_self:
    pdf.set_y(pdf.get_y()+5.0)
    pdf.print_para(selftext,border_size=1)


pdf.ln(5)
pdf.print_line("Comments:\n")
pdf.ln(2)
def print_comments (top_comments):
    counter = 0
    for comment in top_comments:
        if counter == 20:
            return

        pdf.set_x(15.0)
        pdf.print_line("/u/" + comment.author.name + "  " + str(comment.score) + " points  [" + str(datetime.fromtimestamp(comment.created_utc)) + "]\n",border_size=1)
        pdf.print_text(comment.body, 0)
        pdf.ln(5)
        comment_recur(comment,1)
        counter+=1

def comment_recur (comment_tree, level):
    if not comment_tree or comment_tree is None:
        return

    for child in comment_tree.replies:
        if child.author is None:
            continue

        if not child or child is None:
            return

        pdf.print_text("/u/" + child.author.name + "  " + str(child.score) + " points  [" + str(datetime.fromtimestamp(child.created_utc)) + "]\n", level-1, border_size=1)
        pdf.print_text(child.body + "\n\n", level)
        pdf.ln(2)

        comment_recur(child, level+1 )


print_comments(top_level_comments)
pdf.output('test.pdf','F')

print("Done.")

