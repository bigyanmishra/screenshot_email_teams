# Where is my Screenshot?
## 1. Problem Statement
While we have been sending automated emails with PDF export(s) of our BI dashboards, there's always been a subtle ask for including a quick inline screenshot, embedded, within the email body as well.

There are many such BI apps & biz use-cases with similar requirement. But here, at one of our customer, we are limited by available features of MicroStrategy Distribution Services (preferred BI tool). 

## 2. Proposed Solution
To help achieve this, we have written a **3 – part**, **UI-tool-and-platform-independent** Python script, which can: **1) Take screenshots**, **2) Send an email with inline image & PDF attachment**, & **3) Send a customized message on MSFT Teams too**. This can be added to our dashboard data refresh schedule workflow.

## 3. Considerations
1. Script was run on our local environments (as of JAN - 18 - 2021) & we need to test if this can be executed on our customer's servers
1. With no access to customer's SMTP server details, we are currently routing emails via a *secured* Amazon’s Simple Email Service (SES) - SMTP
   1. MSTR Admins can help update this
1.	Email rendering on mobile devices needs some more configs :neutral_face:
1. Message to MSFT – Teams require configuring an incoming webhook

## 4. Workflow
![Simplified Workflow](/images/workflow.JPG)

## 5. Code Walkthrough
### Part I - Taking Screenshot
1. This part refers the *selenium* package to automate web browser interaction from Python. [Python bindings for Selenium](https://pypi.org/project/selenium/)
1. Selenium requires a driver to interface with the chosen browser. In our instance, for Chrome, we have downloaded the [driver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and saved it at a location where we have installed Python on local/server machine (*this step is critical*)
   1. Making sure it is in your *PATH*, e. g., place it in */usr/bin or /usr/local/bin*

**Making Connection to MicroStrategy**

```
mstr_conn = "https://XXXX/MicroStrategyXXX/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID=XXXX&currentViewMedia=1&visMode=0&Server=XXXX&Port=0&share=1&uid=XXXX&pwd=XXXX"
```

Here we have appended uid and pwd in the URL itself. Not so secured, for now, but it works! :upside_down_face:

**Setting Window Size / Resolution**

```
options.add_argument('window-size=1653x1500')
```

Please pass on appropriate window resolution to avoid any scrolls in screenshot

**Selecting Content for Screenshot**

```
driver.find_element_by_id('mstr55')
```

We do not want browser (horizontal) bar, menu bar or any other header(s)/footer(s) in our screenshot. From browser's developer tool, we have picked the exact HTML element ID for which we need the screenshot. This can be made dynamic in future.

### Part II - Sending Email
1. This part refers *smtplib* & *email.utils* along with *base64*
1. `# Comments` within the code will help explain script's flow

### Part III - Sending Message on MSFT Teams
1. This part refers *pymsteams* ([install](https://pypi.org/project/pymsteams/)), which is a Python wrapper library to send requests to Microsoft Teams Webhooks
1. A webhook can be configured on a Teams' Channel from [Get a connector webhook URL for a Microsoft 365 Group](https://docs.microsoft.com/en-us/outlook/actionable-messages/send-via-connectors#creating-messages-through-office-365-connectors-in-microsoft-teams)

## 6. Conclusion
Though this code works for now, it has a huge potential for optimization & security. And, we look forward your thoughts & suggestions. :bow:
