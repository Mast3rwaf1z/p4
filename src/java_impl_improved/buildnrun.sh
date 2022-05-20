rm -r java_impl_improved/build/*

javac -cp java_impl_improved:java_impl_improved/libs/opencv.jar -d java_impl_improved/build java_impl_improved/*.java
java -cp java_impl_improved/build:java_impl_improved/libs/opencv.jar java_impl_improved.subsystem $1 $2 $3