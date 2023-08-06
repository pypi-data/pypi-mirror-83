from distutils.core import setup

setup(
    name='SortStream',
    version='1.2.0',
	author = "Grant Holtes",
	author_email = "gwholes@gmail.com",
	url = "https://github.com/Gholtes/SortStream",
	download_url="https://github.com/Gholtes/SortStream/archive/v1.2.tar.gz",
	keywords = ["nlp", "classification", "document", "pdf"],
    packages=['sortstream'],
	install_requires=[
		"nltk",
		"numpy",
		"PyPDF2",
		"sklearn"
	],
    license="MIT",
	description='NLP Document Classification Tool.'
)
