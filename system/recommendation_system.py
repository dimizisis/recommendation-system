
import ast

class RecommendationSystem:

    def __init__(self, df):
        self.df = df

    def get_recommended_books(self, user, keyword_similarity_method='jaccard'):
        '''
        Given an object of type User, returns recommended books for the specific user
        Optional parameter the keyword_similarity_method, by default is jaccard (alternative: dice)
        '''

        complete_keyword_lst = list()   # the list of user's keyword lists (3 in total)
        for keyword_lst in user.profile['Keywords']:
            complete_keyword_lst.append(ast.literal_eval(keyword_lst))   # get keywords as list

        book_lst = list()   # the list will contain all the books with the similarity
        for index, row in self.df.iterrows():   # for each row of dataframe
            if row['ISBN'] not in user.rated_books: # if user hasn't rated the specific book and the book is not in book list, proceed
                
                curr_keywords = ast.literal_eval(row['Keywords'])
                if keyword_similarity_method == 'jaccard':
                    keyword_similarity_value = self.find_max_jaccard_similarity(complete_keyword_lst, curr_keywords)    # find jaccard similarity value for keyword lists
                elif keyword_similarity_method == 'dice':
                    keyword_similarity_value = self.find_max_dice_coef(complete_keyword_lst, curr_keywords)    # find jaccard similarity value for keyword lists
                else:
                    print('Method not supported. Continuing with jaccard (default)')
                    keyword_similarity_value = self.find_max_jaccard_similarity(complete_keyword_lst, curr_keywords)    # find jaccard similarity value for keyword lists

                author_equality_value = self.get_author_equality_value(user_book_authors=user.profile['Book-Author'], book_author=row['Book-Author'])   # author equality value
                year_diff_value = self.get_min_year_diff_value(user_pub_years=user.profile['Year-Of-Publication'], book_pub_year=row['Year-Of-Publication'])    # year difference value

                similarity_value = self.calc_similarity(keyword_similarity_value, author_equality_value, year_diff_value, keyword_similarity_method)   # similarity value (combiles the 3 values calculated)

                if similarity_value > 0:    # we will not recommend a book with similarity value 0, so no reason to add it to book list         
                    book = {'ISBN': row['ISBN'], 'similarity': similarity_value}
                    book_lst.append({'ISBN': row['ISBN'], 'similarity': similarity_value}) if book not in book_lst else book_lst

        sorted_book_lst = sorted(book_lst, key=lambda k: k['similarity'], reverse=True)

        return sorted_book_lst[:10]
                
    def calc_similarity(self, keyword_similarity_value, author_equality_value, year_diff_value, keyword_similarity_method):
        '''
        Calculates and returns the similarity value (domain: [0,1]) according to the formula given
        '''
        if keyword_similarity_method == 'jaccard':
            return 0.2 * keyword_similarity_value + 0.4 * author_equality_value + 0.4 * year_diff_value
        elif keyword_similarity_method == 'dice':
            return 0.5 * keyword_similarity_value + 0.3 * author_equality_value + 0.2 * year_diff_value


    def get_author_equality_value(self, user_book_authors, book_author):
        '''
        If the author of the book we are looking is
        the same with the author of any of the user's book
        ratings, returns 1
        Else, returns 0
        '''
        author_equality = 0
        for user_book_author in user_book_authors:
            if book_author == user_book_author:
                author_equality = 1 # if book author equality found, stop and return 1
                return author_equality
        return author_equality
                 
    def get_min_year_diff_value(self, user_pub_years, book_pub_year):
        '''
        Calculates the minimum year difference value
        from the formula given (1 - (abs(int(year - book_pub_year)/2005)))
        Returns the value (float)
        '''
        min_year_diff = 2005 # a big number
        year_diff_value = 0
        for year in user_pub_years:
            if abs(year - book_pub_year) < min_year_diff:
                min_year_diff = year - book_pub_year
                year_diff_value = 1 - (abs(int(year - book_pub_year)/2005)) # normalization with given formula
        return year_diff_value    

    def find_max_jaccard_similarity(self, complete_keyword_lst, row_keyword_lst):
        '''
        Finds the maximum jaccard similarity of the user's keyword lists (3 in total) and
        the keyword list of the book we are checking
        Returns the max jaccard similarity value (float)
        '''
        max_value = 0
        for keyword_lst in complete_keyword_lst:
            curr_jaccard_similarity = self.jaccard_similarity(keyword_lst, row_keyword_lst) # for each keyword list (3 in total) calculate the jaccard similarity
            if max_value < curr_jaccard_similarity:
                max_value = curr_jaccard_similarity

        return max_value    # return max similarity

    def find_max_dice_coef(self, complete_keyword_lst, row_keyword_lst):
        '''
        Finds the maximum dice coefficient of the user's keyword lists (3 in total) and
        the keyword list of the book we are checking
        Returns the max dice coefficient value (float)
        '''
        max_value = 0
        for keyword_lst in complete_keyword_lst:
            curr_dice_coef = self.dice_coefficient(keyword_lst, row_keyword_lst)
            if max_value < curr_dice_coef:
                max_value = curr_dice_coef

        return max_value

    def jaccard_similarity(self, list1, list2):
        '''
        Calculates the jaccard similarity of two lists of strings
        and returns it (float)
        '''
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(list1) + len(list2)) - intersection
        return float(intersection) / union

    def dice_coefficient(self, list1, list2):
        '''
        Calculates the dice coefficient of two lists
        and returns it (float)
        '''
        intersection = len(list(set(list1).intersection(list2)))
        return float(2*intersection) / (len(list1) + len(list2))
