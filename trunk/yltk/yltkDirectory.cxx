#include "yltkDirectory.h"
#include <vector>
#include <string>

namespace yltk{
	//----------------------------------------------------------------------------
	class DirectoryInternals
	{
	public:
		// Array of Files
		std::vector<std::string> Files;

		// Path to Open'ed directory
		std::string Path;
	};

	Directory::Directory()
	{
		m_Internal = new DirectoryInternals;
	}

	Directory::~Directory()
	{
		delete m_Internal;
	}

	//----------------------------------------------------------------------------
	const char* Directory::GetPath() const
	{
		return this->m_Internal->Path.c_str();
	}

	//----------------------------------------------------------------------------
	std::vector<std::string>::size_type Directory::GetNumberOfFiles() const
	{
		return this->m_Internal->Files.size();
	}

	void Directory::PrintSelf(std::ostream& os, Indent indent) const
	{
		Superclass::PrintSelf(os, indent);
		os << indent << "Directory for: " << this->GetPath() << "\n";
		os << indent << "Contains the following files:\n";
		indent = indent.GetNextIndent();
		unsigned long numFiles = this->GetNumberOfFiles();
		for ( unsigned long i = 0; i < numFiles; ++i)
		{
			os << indent << this->GetFile(i) << "\n";
		}
	}

	//----------------------------------------------------------------------------
	const char* Directory::GetFile(unsigned long dindex) const
	{
		if ( dindex >= this->m_Internal->Files.size() )
		{
			return 0;
		}
		return this->m_Internal->Files[dindex].c_str();
	}

	//----------------------------------------------------------------------------
	void Directory::Clear()
	{
		this->m_Internal->Path.resize(0);
		this->m_Internal->Files.clear();
	}

	
}

// First microsoft compilers

#if defined(_MSC_VER) || defined(__WATCOMC__)
#include <windows.h>
#include <io.h>
#include <ctype.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

namespace yltk
{

	bool Directory::Load(const char* name)
	{
		this->Clear();
#if _MSC_VER < 1300
		long srchHandle;
#else
		intptr_t srchHandle;
#endif
		char* buf;
		size_t n = strlen(name);
		if ( name[n - 1] == '/' )
		{
			buf = new char[n + 1 + 1];
			sprintf(buf, "%s*", name);
		}
		else
		{
			buf = new char[n + 2 + 1];
			sprintf(buf, "%s/*", name);
		}
		struct _finddata_t data;      // data of current file

		// Now put them into the file array
		srchHandle = _findfirst(buf, &data);
		delete [] buf;

		if ( srchHandle == -1 )
		{
			return 0;
		}

		// Loop through names
		do
		{
			this->m_Internal->Files.push_back(data.name);
		}
		while ( _findnext(srchHandle, &data) != -1 );
		this->m_Internal->Path = name;
		return _findclose(srchHandle) != -1;
	}

	unsigned long Directory::GetNumberOfFilesInDirectory(const char* name)
	{
#if _MSC_VER < 1300
		long srchHandle;
#else
		intptr_t srchHandle;
#endif
		char* buf;
		size_t n = strlen(name);
		if ( name[n - 1] == '/' )
		{
			buf = new char[n + 1 + 1];
			sprintf(buf, "%s*", name);
		}
		else
		{
			buf = new char[n + 2 + 1];
			sprintf(buf, "%s/*", name);
		}
		struct _finddata_t data;      // data of current file

		// Now put them into the file array
		srchHandle = _findfirst(buf, &data);
		delete [] buf;

		if ( srchHandle == -1 )
		{
			return 0;
		}

		// Loop through names
		unsigned long count = 0;
		do
		{
			count++;
		}
		while ( _findnext(srchHandle, &data) != -1 );
		_findclose(srchHandle);
		return count;
	}

} // namespace KWSYS_NAMESPACE

#else

// Now the POSIX style directory access

#include <sys/types.h>
#include <dirent.h>

/* There is a problem with the Portland compiler, large file
support and glibc/Linux system headers: 
http://www.pgroup.com/userforum/viewtopic.php?
p=1992&sid=f16167f51964f1a68fe5041b8eb213b6
*/
#if defined(__PGI) && defined(__USE_FILE_OFFSET64)
# define dirent dirent64
#endif

namespace yltk
{

	bool Directory::Load(const char* name)
	{
		this->Clear();

		if (!name)
		{
			return 0;
		}
		DIR* dir = opendir(name);

		if (!dir)
		{
			return 0;
		}

		for (dirent* d = readdir(dir); d; d = readdir(dir) )
		{
			this->m_Internal->Files.push_back(d->d_name);
		}
		this->m_Internal->Path = name;
		closedir(dir);
		return 1;
	}

	unsigned long Directory::GetNumberOfFilesInDirectory(const char* name)
	{
		DIR* dir = opendir(name);

		if (!dir)
		{
			return 0;
		}

		unsigned long count = 0;
		for (dirent* d = readdir(dir); d; d = readdir(dir) )
		{
			count++;
		}
		closedir(dir);
		return count;
	}

} // namespace KWSYS_NAMESPACE

#endif
