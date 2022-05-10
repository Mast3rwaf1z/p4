rm -r java_impl/build/
rm -r java_impl/*.class

javac -cp java_impl:java_impl/libs/opencv.jar -d java_impl/build java_impl/*.java
java -cp java_impl/build:java_impl/libs/opencv.jar java_impl.subsystem