def buildImage() {
    sh "docker compose build -t moreflix:1.0 ."   
}

return this