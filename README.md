# Contract awards as reported by Kenya's Public Procurement and Oversight Authority (PPOA)
======
The Public Procurement and Disposal Act established the PPOA. It dictates the rules of public tendering in Kenya and specifically for what it terms procuring entities; basically a public entity to which the Act applies.

## Scraping with Python
======
This a Python 2-only repo. Use `python contract_awards.py` in the command line. Trivial to do if you have a Linux variant. Otherwise, if you are a Windows 10 user, don't despair, see [Bash on Ubuntu on Windows]("https://msdn.microsoft.com/en-us/commandline/wsl/install_guide")

### Python libraries needed to be installed via pip

+ Beutiful Soup

## Scraping directly through the command line
======
After ensuring `contract_awards_shell_script` is executable by changing permissions e.g. `chmod +x contract_awards_shell_script`, run `./contract_awards_shell_script`

### Python libraries needed for the command line version
Please see [Jeroen Janssen's Data Science at the Command Line](https://github.com/jeroenjanssens/data-science-at-the-command-line). This repo specifically makes use of:
+ scrape
+ jq
+ xml2json
+ json2csv

Also, you may need to install `ssed`. On Ubuntu, `sudo apt-get update` and `sudo apt-get install ssed` will do the trick. I may have well as used `sed`, but `ssed` is preferable since I'm partial to PCRE regular expressions.

