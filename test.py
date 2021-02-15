from pymongo import MongoClient

client = MongoClient()
print(client.server_info())


@routes.route("/upload", methods=["GET", "POST"])
def test():
    form = UploadForm()
    if form.validate_on_submit():
        df_ref = pd.read_excel(form.item_ref.data, header=1)
        df_ecr = pd.read_excel(form.item_com.data, header=1)
      
        df_ref = df_ref.iloc[:, :-1]
        df_ecr = df_ecr.iloc[:, :-1]
        
        print(df_ref)
        print(df_ecr)

        df_deleted = df_ref.merge(df_ecr, how="outer", indicator=True).loc[
            lambda x: x["_merge"] == "left_only"
        ]      
        df_deleted = df_deleted.reset_index(drop=True)  
        index_deleted = df_deleted.index
        print(df_deleted)
        number_of_rows_deleted = len(index_deleted)

        print(number_of_rows_deleted)
        
        df_new = df_ref.merge(df_ecr, how="outer", indicator=True).loc[
            lambda x: x["_merge"] == "right_only"
        ]
        df_new = df_new.reset_index(drop=True)
        index_new = df_new.index
        print(df_new)
        number_of_rows_new = len(index_new)


        

        # df = pd.concat([df_ref, df_ecr]) 
        # df = df.drop_duplicates(keep=False)  
        # print(df)
        # df = df.reset_index(drop=True)
        
        # df_gpby = df.groupby(list(df.columns))
        
        # idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
        
        return redirect(url_for('routes.index'))
    return render_template("upload.html", form=form)
