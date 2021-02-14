from flask import Blueprint, request, render_template


routes = Blueprint('routes', __name__, url_prefix='/')


@routes.route('/')
def index():
    return "Hallo Welt"


@routes.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        if request.files:
            for input in request.files:
                if input == "file":
                    file = request.files[input]
                    df_1 = pd.read_excel(file, header=1)
                elif input == "newfile":
                    file = request.files[input]
                    df_2 = pd.read_excel(file, header=1)
                elif input == "tech":
                    file = request.files[input]
                    df_tech = pd.read_excel(file)
                    df_tech = df_tech.loc[:, ~
                                          df_tech.columns.str.contains("^Unnamed")]
                    df_tech = df_tech.dropna(subset=["position"])

            # Datenvergleich: Suche nach neuen Features/ Aenderung finden
            new_features = compare_features(new_item)

            # Neue Features -- Vergleich mit Technologien -- Return Features mit Technologien
            feature_techs = get_techs_for_feature(new_features)

            print(df_tech)

            df_1 = df_1.iloc[:, :-1]
            df_2 = df_2.iloc[:, :-1]

            df_deleted = df_1.merge(df_2, how="outer", indicator=True).loc[
                lambda x: x["_merge"] == "left_only"
            ]
            df_deleted = df_deleted.reset_index(drop=True)
            index_deleted = df_deleted.index
            number_of_rows_deleted = len(index_deleted)

            df_new = df_1.merge(df_2, how="outer", indicator=True).loc[
                lambda x: x["_merge"] == "right_only"
            ]
            df_new = df_new.reset_index(drop=True)
            index_new = df_new.index
            number_of_rows_new = len(index_new)

            # print(number_of_rows_deleted)
            # print(number_of_rows_new)

            print(df_deleted, "Sind gelöscht")
            print(df_new, "Kommen neu dazu")

        return render_template(
            "result.html",
            df_deleted=df_deleted,
            df_new=df_new,
            number_of_rows_new=number_of_rows_new,
            number_of_rows_deleted=number_of_rows_deleted,
        )
    return render_template("index.html")
