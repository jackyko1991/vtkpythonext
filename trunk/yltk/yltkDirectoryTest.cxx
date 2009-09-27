#if defined(_MSC_VER)
#pragma warning ( disable : 4786 )
#endif
#include "yltkDirectory.h"

int yltkDirectoryTest(int argc, char *argv[])
{
	yltk::Directory::Pointer directory = yltk::Directory::New();

	if (argc < 2)
	{
		std::cerr << "Usage: " << argv[0] << " directory" << std::endl;
		return EXIT_FAILURE;
	}

	if (directory->Load("qwerty"))
	{
		std::cerr << "directory->Load(\"qwerty\")"
			<< " should have failed." << std::endl;
		return EXIT_FAILURE;
	}
	directory->Load(argv[1]);
	directory->Print(std::cout);

	// Test GetFile with a success and failure
	if (directory->GetNumberOfFiles() > 0)
	{
		std::cout << "File 0 is " << directory->GetFile(0) << std::endl;
	}

	// This should fail
	unsigned int fileOutOfRange = static_cast<unsigned int>( directory->GetNumberOfFiles());
	if (directory->GetFile( fileOutOfRange) )
	{
		std::cerr << "directory->GetFile(directory->GetNumberOfFiles())"
			<< " should have failed." << std::endl;
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}
