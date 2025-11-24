import pandas as pd
import numpy as np
import streamlit as st
import pickle

st.title("Book Recommendation System")

famous_books = pickle.load(open('famous_books1.pkl', 'rb'))


# Function to get Books containing partial name
def search(partial):
    item = []
    for name in famous_books:
        if partial.lower() in name.lower():
            item.append(name)
    return item


ratings = pickle.load(open('ratings11.pkl', 'rb'))
ratings1 = pd.DataFrame(ratings)
pivot = pickle.load(open('pivot1.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores1.pkl', 'rb'))


# Creating Recommendation Function
def recommend(BookName):
    try:
        # index fetch
        index = np.where(pivot.index == BookName)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []
        for i in similar_items:
            item = []
            temp_df = ratings1[ratings1['BookTitle'] == pivot.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('BookTitle')['BookTitle'].values))
            item.extend(list(temp_df.drop_duplicates('BookTitle')['Authors'].values))
            #item.extend(list(temp_df.drop_duplicates('BookTitle')['Description'].values))
            data.append(item)

        return data

    except:
        print("Book Not Found in Database")


top50_books = pickle.load(open('top50books.pkl', 'rb'))

col1, col2 = st.columns([3, 1])

with col1:
    tab1, tab2, tab3 = st.tabs(["Search", "Top50", "Recommendation"])

    with tab1:
        st.header("Search the Title in Database")

        with st.expander("See functionality of this tab"):
            st.write(""" You can search the name of the book you want to recommend even with entering partial name.
            If your search returns nothing in list then it means we don't have that book in our database.""")

        searching_Book = st.text_input('Search a book:', )
        if st.button('Search'):
            found = search(searching_Book)
            if found is not None:
                for i in found:
                    st.write(f"Book Title: {i}")
            st.write("End of list")

    with tab2:
        st.header("Top 50 Books in our list")

        with st.expander("See functionality of this tab"):
            st.write(""" You will get list of top 50 list of books in our database based on average rating 
            provided that book got at least 250 votes""")

        st.dataframe(top50_books)

    with tab3:
        st.header("Recommendation System")

        with st.expander("See functionality of this tab"):
            st.write(""" You can get the names of recommended books based on your entered book.
            We encourage you to check name you entered in Search tab first to check if that book is in our database or 
            name you entered is correct.
            If your search returns ValueError in list then it means we don't have that book in our database.""")

        selected_Book = st.text_input('Select a book:', )
        if st.button('Recommend'):
            recommendations = recommend(selected_Book)
            if recommendations is not None:
                for i in recommendations:
                    st.write(f"Book Title: {i[0]}")
                    st.write(f"\nAuthor: {i[1]}")
                    #st.write(f"\nDescription: {i[2]}")
                    st.write("-" * 10)
            else:
                e = ValueError("Book Not Found in Database")
                st.exception(e)

with col2:
    from PIL import Image

    image = Image.open('C:\\Users\\ameys\\Desktop\\CDAC\\69618_amey\\CDAC_Project\\project_books_reco\\books1.jpeg')

    st.image(image)


# print(ratings1.head())
print(ratings1.shape)
print(pivot.shape)
print(similarity_scores.shape)