FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml ./
COPY maven-settings.xml /root/.m2/settings.xml
RUN mvn -q -e -DskipTests -s /root/.m2/settings.xml dependency:go-offline
COPY src ./src
RUN mvn -q -DskipTests -s /root/.m2/settings.xml package

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
RUN apk add --no-cache curl
COPY --from=build /app/target/qa-backend-0.1.0.jar /app/app.jar
RUN mkdir -p /app/data
EXPOSE 8000
# 使用 shell 形式以支持 JAVA_OPTS 环境变量
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app/app.jar"]
