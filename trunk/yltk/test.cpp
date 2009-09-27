#include "yltkObject.h"
extern int yltkDirectoryTest(int argc, char *argv[]);
extern int yltkMetaDataDictionaryTest(int argc, char *argv[]);
extern int yltkStateMachineTest(int argc, char *argv[]);

int main(int argc, char *argv[]){
	//yltk::Object::New();
	return yltkStateMachineTest(argc, argv);
	//return yltkMetaDataDictionaryTest(argc, argv);
	//return yltkDirectoryTest(argc, argv);
}