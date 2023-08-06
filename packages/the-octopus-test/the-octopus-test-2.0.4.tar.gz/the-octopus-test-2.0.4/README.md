# Octopus Test Automation Framework.

Octopus is a **Free** Test Automation Framework for E2E Testing, that built on python programming language. Using Selenium and APPIUM test automation tools.

Octopus is a Hybrid test automation framework, that combines features of (Modular, Keyword Driven and Data driven).

## Concepts Included:

* Data Driven.

* Keyword Driven.

* Page Object pattern and Page Factory.  [POM ](https://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html)

* Common web page interaction methods.

* Common Mobile App interaction methods.

* Objects shared repository.

* ExtentReport template for reporting.

## Getting started :

### Required Tools

* Microsoft Access database engine 2010. [Access Engine 2010](https://www.microsoft.com/en-sa/download/details.aspx?id=13255)

* Python. [Python](https://www.python.org/downloads/release/python-350/)

* Selenium WebDriver. [seleniumhq.org](https://www.seleniumhq.org/)

* APPIUM. [appium.io](http://appium.io/)

* VS Code python editor.



## Installation

### Supportive Libraries:

* Install Microsoft Access database engine 2010.

* Install Python 3.5 and above.

* Configure python path and pip tools. in windows , open system variables and edit the path variable and add paths.

* Install selenium libraries using pip from command line.

> pip install -U selenium

* Install APPIUM libraries using pip from command line.

> pip install Appium-Python-Client

* Download Selenium Drivers: Selenium requires a driver to interface with the chosen browser.

* Chrome: [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

* Edge: [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

* Firefox: [FireFoxDriver](https://github.com/mozilla/geckodriver/releases)

* Safari: [SafariDriver](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)


### The-Octopus-Test Framework:

* Instal the Octopus Test Framework

> pip install the-octopus-test


## Test Development:

* Clone the sample Test project [The-Octopus-Sample-Test](https://github.com/the-octopus/octopus-sample-test/)

* Please follow the structure and naming of the sample project:

```
    <Octopus Sample Test>
    +------------------------+
    |<resourcses>            |                        
    |    <ChromeDriver>      |
    |    <ChromeDriver>      |
    |    <ChromeDriver>      |
    |    <ChromeDriver>      |
    |    <TestData>          |
    |                        |
    |<test>                  |                        
    |    <pages>             |
    |       loginPage.py     |
    |       homePage.py      |
    |       ....             |
    |       ....             |
    |    <scenarios>         |
    |       testScenarios.py |
    |                        |
    |                        |
    |main.py                 |    
    |                        |
    |<reports>               |
    |                        |
    +------------------------+
```
* Open the project in your prefered IDE, I recommend VS Code editor. 

* Follow the instructions in the [ README.MD ](https://github.com/the-octopus/octopus-sample-test/) file at the sample project.

## Please for more details do not hesitate to contact me at [LinkedIn](https://www.linkedin.com/in/abdelghany-abdelaziz)