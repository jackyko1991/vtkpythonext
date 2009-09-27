#include "yltkObject.h"
extern int yltkDirectoryTest(int argc, char *argv[]);

int main(int argc, char *argv[]){
	yltk::Object::New();
	return yltkDirectoryTest(argc, argv);
}