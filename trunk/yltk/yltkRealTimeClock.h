#ifndef __yltkRealTimeClock_h
#define __yltkRealTimeClock_h

#include "yltkIndent.h"

namespace yltk
{
	/** \class RealTimeClock
	* \brief The RealTimeClock provides a timestamp from a real-time clock
	*
	* This class represents a real-time clock object 
	* and provides a timestamp in platform-independent format.
	*
	* \author Hee-Su Kim, Compute Science Dept. Kyungpook National University,
	Copyright (c) ISC  Insight Software Consortium.  All rights reserved.
	*/

	class RealTimeClock 
	{

	public:

		/** Define the type for the timestamp */
		typedef double        TimeStampType;

		/** Returns a timestamp in milliseconds   e.g. 52.341243 milliseconds */
		static TimeStampType  GetTimeStamp();

		/** Initialize internal variables on the Clock service.
		*  This method must be called at the begining of every
		*  YLTK application. */
		static void Initialize();

		/** Print the object */
		static void Print(std::ostream& os, yltk::Indent indent=0);

		/** Define the type for the frequency of the clock */
		typedef double        FrequencyType;

	protected:

		/** constructor */
		RealTimeClock();

		/** destructor */
		virtual ~RealTimeClock();

		static void PrintSelf( std::ostream& os, yltk::Indent indent );

	private:

		static  FrequencyType    m_Frequency;
		static  TimeStampType    m_Difference;
		static  TimeStampType    m_Origin;

	};

}


#endif