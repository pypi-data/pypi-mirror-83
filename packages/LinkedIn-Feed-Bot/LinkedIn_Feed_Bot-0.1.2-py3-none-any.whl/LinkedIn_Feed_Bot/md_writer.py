import pandas as pd
import io

def feed_template_md(output_filename, input_obj):
    """Writing out a simple template for the feed of LinkedIn.

    Args:
        output_filename (str)
        input (pandas.DataFrame or str): If the input is a str,
         it is assumed its a filepath to a csv file which will be read with pandas.
         If, on the other hand, the input is apandas.DataFrame,
         we will use it directly.

    Returns:
        [Boolean]: Boolean to make sure that the file is closed on our way out.
    """
    if(type(input_obj) != str and type(input_obj) != pd.core.frame.DataFrame):
        raise ValueError('Input must be a str or a pandas.DataFrame')

    if(type(input_obj) == str):
        df = pd.read_csv(input_obj)
    if(type(input_obj) == pd.core.frame.DataFrame):
        df = input_obj

    f = io.open(output_filename, "w", encoding="utf-8")

    f.write('# LinkedIn Feed' + '\n')

    for author, title, post in zip(df.author_name, df.author_title, df.post):
        f.write('### ' + author + '\n')
        f.write('### ' + title + '\n')
        f.write('\n')
        # To adjust the hashtags into the md file.
        post = post.replace('#', '\#')
        f.write(post + '\n')
        f.write('\n')

    f.close()
    return f.closed