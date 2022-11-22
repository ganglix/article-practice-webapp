import difflib
import streamlit as st

def markup(list_str):
    for i in range(0, len(list_str)):
        if ('- ' in list_str[i]):
            list_str[i] = '[Add' + list_str[i] + ']'
            list_str[i] = list_str[i].replace('- ', '->')
        elif ('+ ' in list_str[i]):
            list_str[i] = '[Delete' + list_str[i] + ']'
            list_str[i] = list_str[i].replace('+ ', '->')
        else:
            list_str[i] = list_str[i].replace(' ', '')  # use strip() will remove \n
        list_str_new = list_str
    return list_str_new

def make_comment(mark_num):
    if -10000 < mark_num < 10:
        comment = 'Disaster!'
    if 10 <= mark_num < 30:
        comment = 'Seriously? '
    if 30 <= mark_num < 50:
        comment = 'Well... this is embarrassing.'
    if 50 <= mark_num < 70:
        comment = 'Not too bad!'
    if 70 <= mark_num < 80:
        comment = 'Pretty good!'
    if 80 <= mark_num < 90:
        comment = 'Great job!'
    if 90 <= mark_num < 100:
        comment = 'Fantastic!'
    if mark_num == 100:
        comment = 'King of articles!'
    return comment

st.title("article app")

# user input text

text_input_container = st.empty()
content_old = text_input_container.text_input("text to do").strip()

if content_old != "":
    text_input_container.empty()  # remove the input text after it is done
    st.info("input done. Now copy the text below")


# remove articles
# split, keep \n \r
content = content_old.replace('\r\n', ' Place_Holder[carriage_return]_So_Unique ')
content = content.replace('\n', ' Place_Holder[newline]_So_Unique ')
text = content.split()

wordcount_before = len(text)

# protect exceptions from being removed
for i in range(1, len(text)):  # start from the 2nd element
    if (text[i] == 'lot' or
            text[i] == 'few' or
            text[i] == 'little' or
            text[i] == 'bit'):
        text[i - 1] = text[i - 1] + ('Place_Holder[keyword]_So_Unique')


# article remove function
def remove_word(the_list, val):
    while val in the_list:
        the_list.remove(val)

remove_word(text, 'a')
remove_word(text, 'A')
remove_word(text, 'an')
remove_word(text, 'An')
remove_word(text, 'the')
remove_word(text, 'The')

wordcount_after = len(text)

wordcount_removed = wordcount_before - wordcount_after

# recover exceptions
text = [elem.replace('Place_Holder[keyword]_So_Unique', '') for elem in text]
text = [elem.replace('Place_Holder[newline]_So_Unique', '\n') for elem in text]
text = [elem.replace('Place_Holder[carriage_return]_So_Unique', '\r\n') for elem in text]

no_artical = ' '.join(text)
no_artical = no_artical.replace(' \n \n ', '\n\n')
no_artical = no_artical.replace(' \r\n', '\r\n')
content_no_a = no_artical.replace('\r\n ', '\r\n')

st.write('\n**', wordcount_removed, 'words removed**')
st.write(content_no_a)


text_submit_container = st.empty()
content_submit = text_submit_container.text_area("text to submit", height=300).strip()

if content_submit != "":
    text_submit_container.empty()  # remove the input text after it is done
    st.info(content_submit)

if st.button("mark it"):
    # marking
    # convert \r\n to whitespace to accomodate a/the at the beginning of a line
    text1 = content_old.replace('\r\n', ' ').split(' ')
    text2 = content_submit.replace('\r\n', ' ').split(' ')


    dif = list(difflib.Differ().compare(text1, text2))
    dif1 = markup(dif)

    content_marked = ' '.join(dif1).replace('  ', '\r\n\r\n')

    st.write(content_marked)

    # show marks and comments
    mark_lost = content_marked.count('->') - content_marked.count('] [')

    print(mark_lost)
    try:
        mark_num = round(100. * float(wordcount_removed - mark_lost) / float(wordcount_removed), 1)
    except:
        mark_num = 0.0
    try:
        comment = make_comment(mark_num)
    except:
        comment = None

    mark_final_str = f'Mark: {mark_num} \n {comment}'

    st.write(mark_final_str)



