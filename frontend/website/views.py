from flask import Blueprint, render_template, request, jsonify, Response, session, current_app
import os

# moznost zakomentovat
import sys
sys.path.append('./lekarnicka')
#####################################

views = Blueprint("views", __name__)

PHOTOS_FOLDER = 'photos'

@views.route("/", methods=['GET', 'POST'])
@views.route("/home", methods=['GET', 'POST'])
def home():
    Drugs = []
    # get drugs from DB
    try:
        Drugs = current_app.al.get_all_meds(session["email"])
    except:
        print("something didnt fetch")
        pass
    return render_template("my_aid_kit.html", drugs=Drugs)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route("/add_drug", methods=['GET', 'POST'])
def add_drug():
    try:
        email = session["email"]
    except:
        return render_template('user_not_log.html')

    if request.method == 'POST':
        # Get file from html
        f = request.files['imageUpload']
        if not f:
            return render_template('add_drug.html', error=True)

        img_path = os.path.join(PHOTOS_FOLDER, f.filename)
        f.save(img_path)
        print(img_path)
        al = current_app.al
        result = al.barcode2name(img_path)

        if result == " " or result == "None":
            return render_template('add_drug.html', error=True)

        return render_template('add_drug.html', code=result)

    return render_template("add_drug.html", error="")


@views.route('/recognize_all', methods=['POST'])
def name_recognize():
    if request.method == 'POST':
        er = 1
        print("request received")
        print(request.form)
        if 'action_analyse' in request.form:
            print("analysing photo...")

            # CHECK IF ALLOWED FILE FORMATS SUBMITED
            if 'name_file' in request.files:
                f_name1 = request.files['name_file']
                if f_name1.filename != '':
                    if allowed_file(f_name1.filename):
                        print(f_name1.filename)
                    else:
                        print("not allowed file format - name")
                        print(f_name1.filename)
                        return render_template("add_drug.html", error=3)
            else:
                f_name1 = False
            if 'expiracy_file' in request.files:
                f_exp = request.files['expiracy_file']
                if f_exp.filename != '':
                    if allowed_file(f_exp.filename):
                        print(f_exp.filename)
                    else:
                        print("not allowed file format - expiracy")
                        print(f_exp.filename)
                        return render_template("add_drug.html", error=3)
            else:
                f_exp = False

            # getting name from inputs
            session["name1"] = request.form["input_name1"]
            name2 = " "  # not implemented
            # name2 = request.form['input_name2']
            session["expiracy"] = request.form['input_expiracy']
            print("name1:", session["name1"], "expiracy:", session["expiracy"])

            if f_name1:  # BARCODE SCANNER
                # saves image to photos and returns path
                img_path = save_and_get_path(f_name1)

                # sends the path of the image to backend, backend returns NAME
                al = current_app.al
                result_name1 = al.barcode2name(img_path)

                if result_name1 == "UNKNOWN" or result_name1 == "None":
                    er = 4
                    result_name1 = ''
                    # return render_template("add_drug.html", text_name1=session["name1"],
                    #                        text_name2=name2, text_expiracy=session["expiracy"], error=4)
                session["name1"] = result_name1
                # render_template("add_drug.html", text_name1=session["name1"],
                #                 text_name2=name2, text_expiracy=session["expiracy"])

            # if f_name2:  # 2D CODE SCANNER - backend not working
            #     img_path = save_and_get_path(f_name2)
            #     result_name2 = al.matrixcode2string(img_path)
            #     if result_name2 == " " or result_name2 == "None":
            #         return render_template("add_drug.html", text_name1=name1,
            #                                text_name2=name2, text_expiracy=expiracy, error=True)
            #     name2 = result_name2

            if f_exp:   # EXPIRACY SCANNER
                img_path = save_and_get_path(f_exp)
                al = current_app.al
                result_exp = al.photo2date(img_path)
                print("result_exp:", result_exp)
                if result_exp is None:
                    er = 4
                    result_exp = ''
                    # return render_template("add_drug.html", text_name1=session["name1"],
                    #                        text_name2=name2, text_expiracy=session["expiracy"], error=4)
                session["expiracy"] = result_exp
            print(er)
            if er == 4:
                return render_template("add_drug.html", text_name1=session["name1"],
                                       text_name2=name2, text_expiracy=session["expiracy"], error=4)

            if session["name1"] == "" or session["expiracy"] == "":
                return render_template("add_drug.html", text_name1=session["name1"],
                                       text_name2=name2, text_expiracy=session["expiracy"], error=1)

            # tady už je všechno v cajku

            return render_template("add_drug.html", text_name1=session["name1"],
                                   text_name2=name2, text_expiracy=session["expiracy"], error=2)
        elif "action_send" in request.form:
            # getting name from inputs
            session["name1"] = request.form["input_name1"]
            session["expiracy"] = request.form['input_expiracy']
            print("name1:", session["name1"], "expiracy:", session["expiracy"])

            if session["name1"] == "" or session["expiracy"] == "":  # data missing
                return render_template("add_drug.html", text_name1=session["name1"],
                                       text_expiracy=session["expiracy"], error=1)
            else: # all data present
                al = current_app.al
                try:
                    exp = al.separate_date(session["expiracy"])
                    if exp == None:
                        print("its none")
                        return render_template("add_drug.html", text_name1=session["name1"],
                                               text_expiracy=session["expiracy"], error=6)
                    print("got exp:", exp)
                    if al.add_item_to_lekarnicka(session["email"], session["name1"], exp):
                        print("saved to DB")
                    else:
                        print("something went wrong")
                        return render_template("add_drug.html", text_name1=session["name1"],
                                               text_expiracy=session["expiracy"], error=5)
                except:
                    print("date in the wrong format, try writing it as day.moth.year")
                    return render_template("add_drug.html", text_name1=session["name1"],
                                           text_expiracy=session["expiracy"], error=6)

                return render_template("add_drug.html", text_name1=session["name1"],
                                   text_expiracy=session["expiracy"], error=0)
    else:
        return render_template("add_drug.html", text_name1="", text_name2="", text_expiracy="", error="")

def save_and_get_path(file):
    img_path = os.path.join(PHOTOS_FOLDER, file.filename)
    file.save(img_path)
    return img_path
