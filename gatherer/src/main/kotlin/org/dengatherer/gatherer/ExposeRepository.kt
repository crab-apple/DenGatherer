package org.dengatherer.gatherer;

import org.springframework.context.annotation.Profile
import org.springframework.data.mongodb.repository.MongoRepository

@Profile("dev", "prod")
interface ExposeRepository : MongoRepository<Expose, String> {

}
