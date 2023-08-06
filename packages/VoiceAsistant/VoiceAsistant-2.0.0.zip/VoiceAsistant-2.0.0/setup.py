from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='VoiceAsistant',
  version='2.0.0',
  description='Speak Voice Asistants',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/ilkay-alti/TalkinVoiceAssistant',  
  author='ilkay altınışık',
  author_email='ilkayalti@hotmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ArisaVoiceAsistant', 
  packages=find_packages(),
  install_requires=['selenium','googletrans','playsound','feedparser','requests','wikipedia','gtts','SpeechRecognition==3.8.1',"PyAudio==0.2.11"] 
  
)

