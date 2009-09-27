#ifndef __yltkDirectory_h
#define __yltkDirectory_h

#include "yltkObject.h"
#include <vector>

namespace yltk{
	/** \class Directory
	* \brief Portable directory/filename traversal.
	* 
	* yltk::Directory provides a portable way of finding the names of the files
	* in a system directory.
	*
	* yltk::Directory works with Windows and Unix (POSIX) operating systems.
	* \ingroup OSSystemObjects 
	*
	* 
	*/
	class DirectoryInternals;

	class Directory : public Object{
	public:
		/** Standard class typedefs. */
		typedef Directory                   Self;
		typedef Object                      Superclass;
		typedef SmartPointer<Self>          Pointer;
		typedef SmartPointer<const Self>    ConstPointer;

		/** Method for creation not through the object factory. */
		static Pointer New()
		{ Pointer n = new Self; n->UnRegister(); return n; }

		/** Return the class name as a string. */
		yltkTypeMacro(Directory,Object);

		/** Load the specified directory and load the names of the files
		* in that directory. 0 is returned if the directory can not be 
		* opened, 1 if it is opened.    */
		bool Load(const char* dir);

		/** Return the number of files in the current directory. */
		std::vector<std::string>::size_type GetNumberOfFiles()const;

		/** Return the file at the given index, the indexing is 0 based */
		const char* GetFile(unsigned long index) const;

		/**
		* Return the path to Open'ed directory
		*/
		const char* GetPath() const;

		/**
		* Clear the internal structure. Used internally at beginning of Load(...)
		* to clear the cache.
		*/
		void Clear();

		/**
		* Return the number of files in the specified directory.
		* A higher performance static method.
		*/
		static unsigned long GetNumberOfFilesInDirectory(const char*);

	protected:
		Directory();
		~Directory();
		virtual void PrintSelf(std::ostream& os, Indent indent) const;
	private:
		DirectoryInternals* m_Internal;

		Directory(const Self&); //purposely not implemented
		void operator=(const Self&); //purposely not implemented
	};
}

#endif