#ifndef __yltkVersion_h
#define __yltkVersion_h

#include "yltkObject.h"
#include "yltkObjectFactory.h"

#define YLTK_VERSION "1.0.0"
#define YLTK_SOURCE_VERSION "itkversion 1.0.0"

namespace yltk{
	/** \class Version
	* \brief Track the current version of the software.
	*
	* Holds methods for defining/determining the current yltk version
	* (major, minor, build).
	*
	* This file will change frequently to update the YLTKSourceVersion which
	* timestamps a particular source release.
	*
	* \ingroup YLTKSystemObjects
	*/
	class Version: public Object
	{
	public:
		/** Standard class typedefs. */
		typedef Version                   Self;
		typedef Object                    Superclass;
		typedef SmartPointer<Self>        Pointer;
		typedef SmartPointer<const Self>  ConstPointer;

		/** Method for creation through the object factory. */
		yltkNewMacro(Self);

		/** Standard part of every itk Object. */
		yltkTypeMacro(Version,Object);

		/** Return the version of itk this object is a part of.
		* A variety of methods are included. GetITKSourceVersion returns a string
		* with an identifier which timestamps a particular source tree.  */
		static const char *GetYLTKVersion() { return YLTK_VERSION; }
		static int GetYLTKMajorVersion() { return 1; }
		static int GetYLTKMinorVersion() { return 0; }
		static int GetYLTKBuildVersion() { return 0; }
		static const char *GetYLTKSourceVersion() { return YLTK_SOURCE_VERSION; }

	protected:
		Version();
		~Version();

	private:
		Version(const Self&); //purposely not implemented
		void operator=(const Self&);//purposely not implemented
	};
}

#endif