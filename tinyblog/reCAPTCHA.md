## keys

### Site key

**Use this in the HTML code your site serves to users.**

`6LffkVkUAAAAANsOYU0ou_jejR5g470w_UlDACDP`

### Secret key

**Use this for communication between your site and Google. Be sure to keep it a secret.**

`6LffkVkUAAAAAP8u34LjbMIMazMQkvsnzfKH8tJL`


## Step 1. Client side integration
Paste this snippet before the closing </head> tag on your HTML template:

`<script src='https://www.google.com/recaptcha/api.js'></script>`

Paste this snippet at the end of the <form> where you want the reCAPTCHA widget to appear:

`<div class="g-recaptcha" data-sitekey="6LffkVkUAAAAANsOYU0ou_jejR5g470w_UlDACDP"></div>`


## Step 2. Client side integration

When your users submit the form where you integrated reCAPTCHA, you'll get as part of the payload a string with the name "g-recaptcha-response". In order to check whether Google has verified that user, send a POST request with these parameters:

URL: https://www.google.com/recaptcha/api/siteverify

|            |     |
| ---------- | --- |
|secret (required)  |6LffkVkUAAAAAP8u34LjbMIMazMQkvsnzfKH8tJL|
|response (required)|The value of 'g-recaptcha-response'.    |
|remoteip           |The end user's ip address.              |