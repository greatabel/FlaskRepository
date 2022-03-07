steps:
1. install webapp2 related packages:
pip install -r  requirements.txt 

2. using the Python executable to launch webapp2 website:
python L1_patch.py

then visit:
http://127.0.0.1:8080/
to see we defense L1 level attack.
(L2, L3 ... L6 is just repeat step 2, change "python L1_patch.py" 's py name )


3. test injecture on original site by following:

    when run python L1.py
    input:
    <script>alert()</script>

    when run python L2.py 
    input:
    <img src='x' onerror='alert()'>

    when run python L3.py
    change url into:
    http://127.0.0.1:8080/#1/frame#'onerror='alert(%22Level3%22)'

    when run python L4.py
    input:
    3'**alert());//

    when run python L5.py
    http://127.0.0.1:8080/test/signup?next=javascript:alert()  
    then click " Next>>  "button

    when run python L6.py
    http://127.0.0.1:8080/#data:text/javascript,alert('XSS')



4. test defence on stie by following:

    when run python L1_patch.py
    input:
    <script>alert()</script>

    when run python L2_patch.py 
    input:
    <img src='x' onerror='alert()'>

    when run python L3_patch.py
    change url into
    http://127.0.0.1:8080/#1/frame#'onerror='alert(%22Level3%22)'

    when run python L4_patch.py
    input:
    3'**alert());//

    when run python L5_patch.py
    http://127.0.0.1:8080/test/signup?next=javascript:alert()  
    then click " Next>>  "button

    when run python L6_patch.py
    http://127.0.0.1:8080/#data:text/javascript,alert('XSS')


5. test scp2 / scp3 project:
install flask under python3
pip install Flask
then into "scp" folder, run in terminal: python3 app.py



