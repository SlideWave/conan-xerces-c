#include <xercesc/util/PlatformUtils.hpp>

using namespace xercesc;

int main(void) {
	try {
		XMLPlatformUtils::Initialize();
	}
	catch (const XMLException&) {
		return 1;
	}

	XMLPlatformUtils::Terminate();
	return 0;
}
