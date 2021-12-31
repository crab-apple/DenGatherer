package org.dengatherer.gatherer

import org.springframework.boot.context.event.ApplicationStartedEvent
import org.springframework.context.ApplicationListener
import org.springframework.stereotype.Component

@Component
class StartupListener : ApplicationListener<ApplicationStartedEvent> {
    override fun onApplicationEvent(event: ApplicationStartedEvent) {

        val activeProfiles = event.applicationContext.environment.activeProfiles.toSet()
        val acceptedProfileSets: Set<Set<String>> = setOf(setOf("prod"), setOf("dev"), setOf("test"))

        if (!acceptedProfileSets.contains(activeProfiles)) {
            throw IllegalStateException("Invalid profiles")
        }
    }
}